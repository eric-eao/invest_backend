from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class SnapshotBenchmarkBase(BaseModel):
    benchmark_id: UUID
    date: date
    rate_daily: Optional[float] = None
    rate_monthly: Optional[float] = None
    rate_semester: Optional[float] = None
    rate_yearly: Optional[float] = None
    rate_ytd: Optional[float] = None
    summary_calc_status: Optional[str] = Field("PENDING", max_length=20)

class SnapshotBenchmarkCreate(SnapshotBenchmarkBase):
    pass

class SnapshotBenchmarkUpdate(SnapshotBenchmarkBase):
    pass

class SnapshotBenchmarkOut(SnapshotBenchmarkBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
