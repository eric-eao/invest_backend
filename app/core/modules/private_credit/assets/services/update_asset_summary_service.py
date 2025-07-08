from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.private_credit.private_credit_asset import PrivateCreditAsset
from app.models.positions import Position


def update_private_credit_asset_summaries(db: Session) -> dict:
    try:
        assets = db.query(PrivateCreditAsset).all()

        for asset in assets:
            lots = (
                db.query(Position)
                .filter(Position.asset_id == asset.id, Position.quantity_current > 0)
                .all()
            )

            if not lots:
                continue

            total_quantity = Decimal("0")
            total_invested = Decimal("0")
            total_profitability_amount = Decimal("0")
            weighted_price_sum = Decimal("0")
            weighted_cdi_raw_sum = Decimal("0")
            total_days = Decimal("0")
            total_weighted_days = Decimal("0")
            valuation_dates = []

            for lot in lots:
                q = lot.quantity_current
                if q <= 0:
                    continue

                total_quantity += q
                total_invested += lot.total_invested
                total_profitability_amount += lot.profitability_amount or Decimal("0")
                weighted_price_sum += (lot.current_unit_price or Decimal("0")) * q
                weighted_cdi_raw_sum += (lot.cdi_ref or Decimal("0")) * q

                if lot.lot_start_date and lot.last_valuation_date:
                    days = (lot.last_valuation_date - lot.lot_start_date).days
                    total_days += Decimal(days)
                    total_weighted_days += Decimal(days) * q

                if lot.last_valuation_date:
                    valuation_dates.append(lot.last_valuation_date)

            asset.current_unit_price = (weighted_price_sum / total_quantity).quantize(Decimal("0.01"))
            asset.last_valuation_date = max(valuation_dates)
            asset.profitability_amount = total_profitability_amount.quantize(Decimal("0.01"))

            if total_invested > 0:
                profitability_percent = (total_profitability_amount / total_invested) * 100
                asset.profitability_percent = profitability_percent.quantize(Decimal("0.01"))
            else:
                profitability_percent = None
                asset.profitability_percent = None

            # CDI médio ponderado no período (acumulado, em %)
            cdi_avg = (weighted_cdi_raw_sum / total_quantity) if total_quantity > 0 else None

            # ➕ Calcula quantos % do CDI o ativo rendeu
            if cdi_avg and cdi_avg > 0 and profitability_percent is not None:
                rel_cdi_percent = (profitability_percent / cdi_avg) * 100
                asset.cdi_ref = rel_cdi_percent.quantize(Decimal("0.01"))
            else:
                asset.cdi_ref = None

            # Rentabilidade anualizada
            if total_weighted_days > 0 and total_invested > 0:
                fator_total = (total_invested + total_profitability_amount) / total_invested
                media_dias = total_weighted_days / total_quantity
                anualizada = (fator_total ** (Decimal("365") / media_dias) - 1) * 100
                asset.profitability_percent_annualized = anualizada.quantize(Decimal("0.01"))
            else:
                asset.profitability_percent_annualized = None

            db.add(asset)

        db.commit()
        return {"message": "Resumo dos ativos atualizado com sucesso."}

    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao atualizar resumo dos ativos: {str(e)}")
