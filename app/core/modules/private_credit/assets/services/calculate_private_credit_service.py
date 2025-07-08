from sqlalchemy.orm import Session
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
import pandas as pd

from app.core.utils.calendar.brazil_holiday_calendar import get_brazil_business_day
from app.models.positions import Position
from app.models.snapshot.snapshot_benchmark import SnapshotBenchmark
from app.models.control.control_benchmark import ControlBenchmark
from app.schemas.enums import RateType, Indexer
from pandas.tseries.offsets import CustomBusinessDay


def calculate_private_credit_service(db: Session) -> dict:
    try:
        today = date.today()
        lots = db.query(Position).filter(Position.quantity_current > 0).all()

        brazil_bday = get_brazil_business_day()

        # 🔎 Benchmark ID fixo para CDI
        cdi_benchmark_id = db.query(ControlBenchmark.id).filter(ControlBenchmark.name == "CDI").scalar()

        for lot in lots:
            asset = lot.asset
            days_diff = len(pd.date_range(lot.lot_start_date, today, freq=brazil_bday))

            print(f"\n🧾 LOTE ID: {lot.id}")
            print(f"Asset: {asset.code} | RateType: {asset.rate_type} | Indexer: {asset.indexer}")
            print(f"Data início: {lot.lot_start_date} | Hoje: {today} | Dias úteis reais: {days_diff}")
            print(f"Preço inicial do lote: {lot.unit_price_initial}")
            print(f"Quantidade atual do lote: {lot.quantity_current}")

            pu = None

            if asset.rate_type == RateType.PREFIXADO:
                fixed_rate = Decimal(asset.fixed_rate or 0)
                base = Decimal("1") + (fixed_rate / Decimal("100"))
                exponent = Decimal(days_diff) / Decimal("252")
                pu = lot.unit_price_initial * base ** exponent

                print(f"[PREFIXADO] Fixed rate anual: {fixed_rate}%")
                print(f"[PREFIXADO] PU (composto): {pu:.6f}")

            elif asset.indexer == Indexer.CDI:
                pu = calculate_pu_from_cdi(
                    db=db,
                    benchmark_id=cdi_benchmark_id,
                    start_date=lot.lot_start_date,
                    end_date=today,
                    unit_price_initial=lot.unit_price_initial,
                    index_percent=asset.index_percent,
                )
                print(f"[CDI] PU calculado: {pu:.6f}")

            elif asset.indexer == Indexer.IPCA:
                pu = calculate_pu_from_ipca(
                    db=db,
                    asset=asset,
                    start_date=lot.lot_start_date,
                    end_date=today,
                    unit_price_initial=lot.unit_price_initial,
                    custom_bday=brazil_bday,
                )
                print(f"[IPCA] PU calculado: {pu:.6f}")

            if pu is None:
                print("⚠️ PU não calculado (indexador não suportado ou ativo inválido)")
                continue

            pu = pu.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            initial_price = lot.unit_price_initial

            # 💰 Rentabilidade do lote
            profitability_percent = ((pu - initial_price) / initial_price) * 100 if initial_price > 0 else Decimal(0)
            profitability_amount = (pu - initial_price) * lot.quantity_current

            # 📊 CDI acumulado no mesmo período
            cdi_rates = (
                db.query(SnapshotBenchmark.rate_daily)
                .filter(
                    SnapshotBenchmark.benchmark_id == cdi_benchmark_id,
                    SnapshotBenchmark.date >= lot.lot_start_date,
                    SnapshotBenchmark.date <= today,
                )
                .order_by(SnapshotBenchmark.date)
                .all()
            )

            cdi_factor = Decimal("1")
            for (rate,) in cdi_rates:
                cdi_factor *= (1 + (rate / Decimal("100")))

            cdi_percent = (cdi_factor - 1) * 100
            lot.cdi_ref = cdi_percent.quantize(Decimal("0.01"))

            print(f"CDI no período do lote: {lot.cdi_ref}%")

            # Comparação com CDI
            if lot.cdi_ref and lot.cdi_ref > 0:
                percent_vs_cdi = profitability_percent / lot.cdi_ref * 100
                print(f"→ Ativo rendeu {percent_vs_cdi:.2f}% do CDI no período")

            # Atualização dos campos
            lot.current_unit_price = pu
            lot.profitability_percent = profitability_percent.quantize(Decimal("0.01"))
            lot.profitability_amount = profitability_amount.quantize(Decimal("0.01"))
            lot.last_valuation_date = today

            db.add(lot)

        db.commit()
        return {"message": "Rentabilidade por lote calculada com sucesso."}

    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao calcular rentabilidade por lote: {str(e)}")


def calculate_pu_from_cdi(
    db: Session,
    benchmark_id: int,
    start_date: date,
    end_date: date,
    unit_price_initial: Decimal,
    index_percent: Decimal = None
) -> Decimal:
    daily_rates = (
        db.query(SnapshotBenchmark.rate_daily)
        .filter(
            SnapshotBenchmark.benchmark_id == benchmark_id,
            SnapshotBenchmark.date >= start_date,
            SnapshotBenchmark.date <= end_date,
        )
        .order_by(SnapshotBenchmark.date)
        .all()
    )

    factor = Decimal("1")
    index_factor = (Decimal(index_percent or 100)) / Decimal("100")

    for (rate,) in daily_rates:
        factor *= (1 + (rate / Decimal("100")) * index_factor)

    return unit_price_initial * factor


def calculate_pu_from_ipca(
    db: Session,
    asset,
    start_date: date,
    end_date: date,
    unit_price_initial: Decimal,
    custom_bday: CustomBusinessDay
) -> Decimal:
    benchmark_id = (
        db.query(ControlBenchmark.id)
        .filter(ControlBenchmark.name == "IPCA")
        .scalar_subquery()
    )

    daily_rates = (
        db.query(SnapshotBenchmark.rate_daily)
        .filter(
            SnapshotBenchmark.benchmark_id == benchmark_id,
            SnapshotBenchmark.date >= start_date,
            SnapshotBenchmark.date <= end_date,
        )
        .order_by(SnapshotBenchmark.date)
        .all()
    )

    if not daily_rates:
        raise Exception("Sem dados de IPCA para o período")

    # ✅ Fator IPCA acumulado com composição de taxa diária
    factor_ipca = Decimal("1")
    for (rate,) in daily_rates:
        rate_decimal = rate / Decimal("100")
        factor_ipca *= (1 + rate_decimal)

    # ✅ Composição do spread
    spread = Decimal(asset.spread or 0)
    days = len(pd.date_range(start_date, end_date, freq=custom_bday))
    factor_spread = (1 + (spread / Decimal("100")) / Decimal("252")) ** Decimal(days)

    return unit_price_initial * factor_ipca * factor_spread
