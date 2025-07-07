import uuid
from sqlalchemy import Column, Date, Numeric, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class SnapshotBenchmark(Base):
    __tablename__ = "snapshot_benchmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    benchmark_id = Column(UUID(as_uuid=True), ForeignKey("control_benchmarks.id"), nullable=False)
    date = Column(Date, nullable=False)
    rate_daily = Column(Numeric(20,6), nullable=True)
    rate_monthly = Column(Numeric(20,6), nullable=True)
    rate_semester = Column(Numeric(20,6), nullable=True)
    rate_yearly = Column(Numeric(20,6), nullable=True)
    rate_ytd = Column(Numeric(20,6), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    summary_calc_status = Column(String(20), nullable=False, default="PENDING")