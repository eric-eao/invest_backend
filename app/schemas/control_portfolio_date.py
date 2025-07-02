from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional

from app.schemas.control_module import ControlModuleOut

class ControlPortfolioDateBase(BaseModel):
    module_id: UUID
    first_investiment: Optional[date] = None
    last_investiment: Optional[date] = None
    active: bool = True

class ControlPortfolioDateCreate(ControlPortfolioDateBase):
    pass

class ControlPortfolioDateUpdate(BaseModel):
    first_investiment: Optional[date] = None
    last_investiment: Optional[date] = None
    active: Optional[bool] = None

class ControlPortfolioDateOut(ControlPortfolioDateBase):
    id: UUID
    updated_at: datetime
    module: ControlModuleOut

    class Config:
        from_attributes = True
