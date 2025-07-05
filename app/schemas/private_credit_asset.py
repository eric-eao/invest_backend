from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime, date
from app.schemas.movement import MovementCreate

class PrivateCreditAssetBase(BaseModel):
    description: str
    code: str
    institution: str
    category_id: UUID
    maturity_date: Optional[date]
    rate_type: Optional[str]           # <-- corrigido para Optional
    indexer: Optional[str]
    fixed_rate: Optional[float]
    spread: Optional[float]
    index_percent: Optional[float]
    active: bool = True

class PrivateCreditAssetCreate(PrivateCreditAssetBase):
    initial_movement: Optional[MovementCreate] = None

class PrivateCreditAssetUpdate(BaseModel):
    description: Optional[str] = None
    code: Optional[str] = None
    institution: Optional[str] = None
    category_id: Optional[UUID] = None
    maturity_date: Optional[date] = None
    rate_type: Optional[str] = None
    indexer: Optional[str] = None
    fixed_rate: Optional[float] = None
    spread: Optional[float] = None
    index_percent: Optional[float] = None
    active: Optional[bool] = None

class PrivateCreditAssetOut(PrivateCreditAssetBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
