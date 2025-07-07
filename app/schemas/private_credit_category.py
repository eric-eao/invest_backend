from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from app.models.enums import CurrencyEnum


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    allocation_planned: float = Field(..., ge=0, le=100)
    currency: CurrencyEnum
    active: Optional[bool] = True
    module_id: UUID  # <-- agora vira UUID, vinculando FK

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    allocation_planned: Optional[float] = Field(None, ge=0, le=100)
    currency: Optional[CurrencyEnum] = None
    active: Optional[bool] = None
    module_id: Optional[UUID] = None  # também ajusta no update

class CategoryOut(CategoryBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
