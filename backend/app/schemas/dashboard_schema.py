from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_submissions: int
    pending_approval: int
    total_trend: Optional[float] = None
    by_status: Dict[str, int]


class RecentActivityItem(BaseModel):
    id: int
    title: str
    actor: str
    status: str
    status_label: str
    created_at: datetime

    class Config:
        from_attributes = True