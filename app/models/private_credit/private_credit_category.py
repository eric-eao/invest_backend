import uuid
from sqlalchemy import Column, String, Float, Boolean, Enum, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.schemas.enums import CurrencyEnum

class Category(Base):
    __tablename__ = "private_credit_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    allocation_planned = Column(Float, nullable=False)
    currency = Column(Enum(CurrencyEnum, name="currency_enum"), nullable=False, default=CurrencyEnum.BRL)
    active = Column(Boolean, default=True, nullable=False)
    
    module_id = Column(UUID(as_uuid=True), ForeignKey("control_modules.id"), nullable=False)

    module = relationship("ControlModule", backref="categories")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "module_id", name="uix_category_name_module_id"),
        {"sqlite_autoincrement": True},
    )