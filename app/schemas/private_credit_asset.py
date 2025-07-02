from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime, date

class PrivateCreditAssetBase(BaseModel):
    description: str
    code: str
    institution: str
    category_id: UUID
    maturity_date: Optional[date]
    rate_type: str
    indexer: Optional[str]
    fixed_rate: Optional[float]
    spread: Optional[float]
    index_percent: Optional[float]
    active: bool = True

class PrivateCreditAssetCreate(PrivateCreditAssetBase):
    pass

class PrivateCreditAssetUpdate(BaseModel):
    description: Optional[str]
    code: Optional[str]
    institution: Optional[str]
    category_id: Optional[UUID]
    maturity_date: Optional[date]
    rate_type: Optional[str]
    indexer: Optional[str]
    fixed_rate: Optional[float]
    spread: Optional[float]
    index_percent: Optional[float]
    active: Optional[bool]

class PrivateCreditAssetOut(PrivateCreditAssetBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
