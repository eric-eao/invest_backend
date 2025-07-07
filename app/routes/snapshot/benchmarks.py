from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.core.modules.snapshot.handlers.snapshot_sync_handler import sync_snapshots_handler

router = APIRouter(
    tags=["snapshot_benchmarks"],
)


@router.post("/sync/{module_id}")
async def sync_snapshots(module_id: UUID, db: Session = Depends(get_db)):
    return await sync_snapshots_handler(db, module_id)