import uuid
from sqlalchemy import Column, String, Date, DECIMAL, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Position(Base):
    __tablename__ = "private_credit_positions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    asset_id = Column(UUID(as_uuid=True), nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("control_modules.id"), nullable=False)

    quantity_initial = Column(DECIMAL(20, 6), nullable=False)
    quantity_current = Column(DECIMAL(20, 6), nullable=False)
    unit_price_initial = Column(DECIMAL(20, 6), nullable=False)
    total_invested = Column(DECIMAL(20, 6), nullable=False)

    lot_start_date = Column(Date, nullable=False)      # data do aporte
    lot_end_date = Column(Date, nullable=True)         # se liquidado
    current_unit_price = Column(DECIMAL(20, 6), nullable=True)
    profitability_percent = Column(DECIMAL(20, 6), nullable=True)
    profitability_amount = Column(DECIMAL(20, 6), nullable=True)

    last_valuation_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
