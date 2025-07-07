import uuid
from sqlalchemy import Column, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ControlPortfolioDate(Base):
    __tablename__ = "control_portfolio_dates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("control_modules.id"), nullable=False)
    first_investment = Column(Date, nullable=True)
    last_investment = Column(Date, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    module = relationship("ControlModule", backref="portfolio_dates")
