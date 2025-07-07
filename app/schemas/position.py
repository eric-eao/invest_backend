from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class PositionBase(BaseModel):
    asset_id: UUID
    module_id: UUID
    quantity_initial: float
    quantity_current: float
    unit_price_initial: float
    total_invested: float
    lot_start_date: date
    lot_end_date: Optional[date] = None
    current_unit_price: Optional[float] = None
    profitability_percent: Optional[float] = None
    profitability_amount: Optional[float] = None
    last_valuation_date: Optional[date] = None

class PositionCreate(PositionBase):
    pass

class PositionUpdate(BaseModel):
    quantity_current: Optional[float] = None
    current_unit_price: Optional[float] = None
    profitability_percent: Optional[float] = None
    profitability_amount: Optional[float] = None
    last_valuation_date: Optional[date] = None
    lot_end_date: Optional[date] = None

class PositionOut(PositionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
