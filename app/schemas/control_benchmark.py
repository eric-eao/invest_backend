from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum

from app.schemas.enums import RatePeriod


class ControlBenchmarkBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    active: Optional[bool] = True
    api_url: Optional[str] = Field(None, max_length=255)
    rate_period: RatePeriod = Field(..., description="Período de referência da taxa (daily, monthly, annual)")
    
class ControlBenchmarkCreate(ControlBenchmarkBase):
    pass

class ControlBenchmarkUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    active: Optional[bool] = None
    api_url: Optional[str] = Field(None, max_length=255)
    rate_period: Optional[RatePeriod] = None
    
class ControlBenchmarkOut(ControlBenchmarkBase):
    id: UUID
    sync_status: str
    sync_from: Optional[datetime]
    sync_to: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
