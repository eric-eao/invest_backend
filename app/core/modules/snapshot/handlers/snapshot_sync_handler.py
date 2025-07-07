from sqlalchemy.orm import Session
from app.core.modules.snapshot.services.snapshot_sync_service import snapshot_sync_service

async def sync_snapshots_handler(db: Session, module_id: str):
    return await snapshot_sync_service(db, module_id)
