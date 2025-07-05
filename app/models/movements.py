import uuid
from sqlalchemy import Column, String, Date, DECIMAL, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import enum

class MovementType(str, enum.Enum):
    APORTE = "APORTE"
    RESGATE_TOTAL = "RESGATE_TOTAL"
    RESGATE_PARCIAL = "RESGATE_PARCIAL"

class MovementStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Movement(Base):
    __tablename__ = "movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    asset_id = Column(UUID(as_uuid=True), nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("control_modules.id"), nullable=False)
    movement_type = Column(Enum(MovementType, name="movement_type_enum"), nullable=False)
    quantity = Column(DECIMAL(20, 6), nullable=False)
    unit_price = Column(DECIMAL(20, 6), nullable=False)
    amount = Column(DECIMAL(20, 6), nullable=False)
    movement_date = Column(Date, nullable=False)
    settlement_date = Column(Date, nullable=True)
    broker = Column(String(255), nullable=True)
    transaction_reference = Column(String(255), nullable=True)
    status = Column(Enum(MovementStatus, name="movement_status_enum"), nullable=False, default=MovementStatus.PENDING)
    notes = Column(String, nullable=True)
    source = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
