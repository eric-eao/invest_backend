from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db

# importe explicitamente os modelos que você JÁ TEM
from app.models.control.control_benchmark import ControlBenchmark
from app.models.snapshot.snapshot_benchmark import SnapshotBenchmark
from app.models.control.control_portfolio_date import ControlPortfolioDate
from app.services.export_table_excel import export_table_excel



router = APIRouter(tags=["exports"])

MODEL_MAP = {
    "control_benchmarks": ControlBenchmark,
    "snapshot_benchmarks": SnapshotBenchmark,
    "control_portfolio_dates": ControlPortfolioDate,
    # adicione outros modelos que você for criando aqui
}

@router.get("/{table_name}", summary="Exportar dados genéricos em Excel")
def export_generic(table_name: str, db: Session = Depends(get_db)):
    model = MODEL_MAP.get(table_name)
    if not model:
        raise HTTPException(status_code=400, detail="Tabela não suportada para exportação.")
    
    return export_table_excel(db, model, filename=table_name)
