from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from app.models.control_benchmark import ControlBenchmark
from app.schemas.control_benchmark import ControlBenchmarkCreate, ControlBenchmarkUpdate

def list_benchmarks(db: Session):
    return db.query(ControlBenchmark).all()

def get_benchmark(db: Session, benchmark_id: UUID):
    benchmark = db.query(ControlBenchmark).filter(ControlBenchmark.id == benchmark_id).first()
    if not benchmark:
        raise HTTPException(status_code=404, detail="Benchmark não encontrado")
    return benchmark

def create_benchmark(db: Session, benchmark_in: ControlBenchmarkCreate):
    db_benchmark = ControlBenchmark(**benchmark_in.dict())
    db.add(db_benchmark)
    db.commit()
    db.refresh(db_benchmark)
    return db_benchmark

def update_benchmark(db: Session, benchmark_id: UUID, updates: ControlBenchmarkUpdate):
    benchmark = db.query(ControlBenchmark).filter(ControlBenchmark.id == benchmark_id).first()
    if not benchmark:
        raise HTTPException(status_code=404, detail="Benchmark não encontrado")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(benchmark, field, value)
    db.commit()
    db.refresh(benchmark)
    return benchmark

def delete_benchmark(db: Session, benchmark_id: UUID):
    benchmark = db.query(ControlBenchmark).filter(ControlBenchmark.id == benchmark_id).first()
    if not benchmark:
        raise HTTPException(status_code=404, detail="Benchmark não encontrado")
    db.delete(benchmark)
    db.commit()
