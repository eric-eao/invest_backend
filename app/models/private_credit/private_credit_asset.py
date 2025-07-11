import uuid
from sqlalchemy import Column, String, Boolean, Date, Float, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class PrivateCreditAsset(Base):
    __tablename__ = "private_credit_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    description = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    institution = Column(String(100), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("private_credit_categories.id"), nullable=False)
    maturity_date = Column(Date, nullable=True)
    rate_type = Column(String(20), nullable=False)
    indexer = Column(String(20), nullable=True)
    fixed_rate = Column(Float, nullable=True)
    spread = Column(Float, nullable=True)
    index_percent = Column(Float, nullable=True)
    module_id = Column(UUID(as_uuid=True), ForeignKey("control_modules.id"), nullable=False)

    # CAMPOS DE RESUMO DE MOVIMENTOS
    total_quantity = Column(Numeric(20, 6), nullable=True)
    total_cost = Column(Numeric(20, 6), nullable=True)
    average_unit_price = Column(Numeric(20, 6), nullable=True)

    # CAMPOS DE MARK-TO-MARKET
    current_unit_price = Column(Numeric(20, 6), nullable=True)
    last_valuation_date = Column(Date, nullable=True)
    profitability_percent = Column(Numeric(20, 6), nullable=True)
    profitability_amount = Column(Numeric(20, 6), nullable=True)
    profitability_percent_annualized = Column(Numeric(20, 6), nullable=True)  # 🆕 Novo campo
    cdi_ref = Column(Numeric(20, 6), nullable=True)  # 🆕 Novo campo

    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

# 👇 Relacionamento atrasado para evitar import circular
from sqlalchemy.orm import relationship
PrivateCreditAsset.positions = relationship("Position", back_populates="asset")
