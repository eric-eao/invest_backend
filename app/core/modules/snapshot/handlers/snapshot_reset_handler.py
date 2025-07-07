from sqlalchemy.orm import Session
from uuid import UUID
from app.core.modules.snapshot.services.snapshot_reset_service import reset_snapshots_service

def snapshot_reset_handler(db: Session, benchmark_id: UUID):
    return reset_snapshots_service(db, benchmark_id)
