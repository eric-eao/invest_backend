from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import httpx
import calendar

from app.models.control.control_benchmark import ControlBenchmark
from app.models.control.control_portfolio_date import ControlPortfolioDate
from app.models.snapshot.snapshot_benchmark import SnapshotBenchmark

async def snapshot_sync_service(db: Session, module_id: str):
    try:
        benchmarks = db.query(ControlBenchmark).filter(ControlBenchmark.active == True).all()
        if not benchmarks:
            return {"message": "Nenhum benchmark ativo para sincronizar."}

        today = date.today()

        portfolio_date = (
            db.query(ControlPortfolioDate)
            .filter(ControlPortfolioDate.module_id == module_id)
            .first()
        )

        if not portfolio_date or not portfolio_date.first_investment:
            raise Exception(f"Data inicial não definida em control_portfolio_dates para módulo {module_id}")

        start_date = portfolio_date.first_investment

        async with httpx.AsyncClient() as client:
            for benchmark in benchmarks:
                url = benchmark.api_url.format(
                    start_date=start_date.strftime("%d/%m/%Y"),
                    end_date=today.strftime("%d/%m/%Y")
                )
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                for item in data:
                    snapshot_date = datetime.strptime(item["data"], "%d/%m/%Y").date()

                    if benchmark.rate_period == "daily":
                        rate_daily = float(item["valor"])

                        snapshot = (
                            db.query(SnapshotBenchmark)
                            .filter(
                                SnapshotBenchmark.benchmark_id == benchmark.id,
                                SnapshotBenchmark.date == snapshot_date
                            )
                            .first()
                        )
                        if not snapshot:
                            snapshot = SnapshotBenchmark(
                                benchmark_id=benchmark.id,
                                date=snapshot_date,
                                rate_daily=rate_daily,
                            )
                            db.add(snapshot)
                        else:
                            snapshot.rate_daily = rate_daily

                    elif benchmark.rate_period == "monthly":
                        valor_decimal = float(item["valor"]) / 100
                        fator_diario = (1 + valor_decimal) ** (1/21) - 1
                        rate_daily = fator_diario * 100

                        year = snapshot_date.year
                        month = snapshot_date.month
                        _, last_day = calendar.monthrange(year, month)
                        current_day = date(year, month, 1)
                        added_days = 0

                        while current_day <= date(year, month, last_day):
                            if current_day.weekday() < 5:
                                snapshot = (
                                    db.query(SnapshotBenchmark)
                                    .filter(
                                        SnapshotBenchmark.benchmark_id == benchmark.id,
                                        SnapshotBenchmark.date == current_day
                                    )
                                    .first()
                                )
                                if not snapshot:
                                    snapshot = SnapshotBenchmark(
                                        benchmark_id=benchmark.id,
                                        date=current_day,
                                        rate_daily=rate_daily,
                                    )
                                    db.add(snapshot)
                                else:
                                    snapshot.rate_daily = rate_daily

                                added_days += 1
                                if added_days >= 21:
                                    break

                            current_day += timedelta(days=1)

                    elif benchmark.rate_period == "annual":
                        valor_decimal = float(item["valor"]) / 100
                        fator_diario = (1 + valor_decimal) ** (1/252) - 1
                        rate_daily = fator_diario * 100

                        snapshot = (
                            db.query(SnapshotBenchmark)
                            .filter(
                                SnapshotBenchmark.benchmark_id == benchmark.id,
                                SnapshotBenchmark.date == snapshot_date
                            )
                            .first()
                        )
                        if not snapshot:
                            snapshot = SnapshotBenchmark(
                                benchmark_id=benchmark.id,
                                date=snapshot_date,
                                rate_daily=rate_daily,
                            )
                            db.add(snapshot)
                        else:
                            snapshot.rate_daily = rate_daily

                    else:
                        raise Exception(f"rate_period desconhecido: {benchmark.rate_period}")

                benchmark.sync_status = "OK"

        db.commit()
        return {"message": "Snapshots sincronizados com sucesso."}

    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao sincronizar benchmarks: {str(e)}")
