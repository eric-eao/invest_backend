from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class ControlModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    active: bool = True
    sync_status: str = "pending"

class ControlModuleCreate(ControlModuleBase):
    pass

class ControlModuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    sync_status: Optional[str] = None
    last_sync_at: Optional[datetime] = None

class ControlModuleOut(ControlModuleBase):
    id: UUID
    last_sync_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
