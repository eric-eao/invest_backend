import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class ControlBenchmark(Base):
    __tablename__ = "control_benchmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    api_url = Column(String(255), nullable=True)
    sync_status = Column(String(20), default="pending", nullable=False)
    sync_from = Column(DateTime(timezone=True), nullable=True)
    sync_to = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    rate_period = Column(String(20), nullable=False, default="daily")