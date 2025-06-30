from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from app.models.enums import CurrencyEnum

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    allocation_planned: float = Field(..., ge=0, le=100)
    currency: CurrencyEnum
    active: Optional[bool] = True
    module: str = Field(..., max_length=50)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    allocation_planned: Optional[float] = Field(None, ge=0, le=100)
    currency: Optional[CurrencyEnum]
    active: Optional[bool]
    module: Optional[str] = Field(None, max_length=50)

class CategoryOut(CategoryBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
