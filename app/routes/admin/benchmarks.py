from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.db.session import get_db
from app.core.modules.control.handlers import benchmark_handler
from app.schemas.control_benchmark import ControlBenchmarkCreate, ControlBenchmarkUpdate, ControlBenchmarkOut

router = APIRouter(tags=["Admin - Benchmarks"])

@router.get("/", response_model=list[ControlBenchmarkOut])
def list_benchmarks(db: Session = Depends(get_db)):
    return benchmark_handler.list_benchmarks(db)

@router.get("/{benchmark_id}", response_model=ControlBenchmarkOut)
def get_benchmark(benchmark_id: UUID, db: Session = Depends(get_db)):
    return benchmark_handler.get_benchmark(db, benchmark_id)

@router.post("/", response_model=ControlBenchmarkOut, status_code=201)
def create_benchmark(benchmark_in: ControlBenchmarkCreate, db: Session = Depends(get_db)):
    return benchmark_handler.create_benchmark(db, benchmark_in)

@router.patch("/{benchmark_id}", response_model=ControlBenchmarkOut)
def update_benchmark(benchmark_id: UUID, updates: ControlBenchmarkUpdate, db: Session = Depends(get_db)):
    return benchmark_handler.update_benchmark(db, benchmark_id, updates)

@router.delete("/{benchmark_id}", status_code=204)
def delete_benchmark(benchmark_id: UUID, db: Session = Depends(get_db)):
    benchmark_handler.delete_benchmark(db, benchmark_id)
    return
