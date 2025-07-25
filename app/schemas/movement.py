from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

from app.schemas.enums import MovementStatus, MovementType

class MovementBase(BaseModel):
    asset_id: UUID
    module_id: UUID
    movement_type: MovementType
    quantity: float
    unit_price: float
    movement_date: date
    settlement_date: Optional[date] = None
    broker: Optional[str] = None
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None

class MovementCreate(MovementBase):
    pass  # sem id no momento de criação

class MovementUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    movement_date: Optional[date] = None
    settlement_date: Optional[date] = None
    broker: Optional[str] = None
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[MovementStatus] = None
    source: Optional[str] = None

class MovementOut(MovementBase):
    id: UUID
    amount: float
    status: MovementStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PrivateCreditInitialMovementCreate(BaseModel):
    module_id: Optional[UUID] = None
    movement_type: str
    quantity: float
    unit_price: float
    movement_date: date
    settlement_date: date
    broker: Optional[str] = None
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None
