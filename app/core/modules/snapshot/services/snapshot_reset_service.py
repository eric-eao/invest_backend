from sqlalchemy.orm import Session
from uuid import UUID
from app.models.control.control_benchmark import ControlBenchmark
from app.models.snapshot.snapshot_benchmark import SnapshotBenchmark

def reset_snapshots_service(db: Session, benchmark_id: UUID):
    try:
        deleted = db.query(SnapshotBenchmark).filter(
            SnapshotBenchmark.benchmark_id == benchmark_id
        ).delete()

        benchmark = db.query(ControlBenchmark).filter(
            ControlBenchmark.id == benchmark_id
        ).first()

        if not benchmark:
            raise Exception("Benchmark não encontrado.")

        benchmark.sync_status = "PENDING"
        db.commit()

        return {
            "message": f"{deleted} snapshots removidos, benchmark pronto para nova sincronização."
        }

    except Exception as e:
        db.rollback()
        raise Exception(f"Erro ao resetar benchmark: {str(e)}")
