from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ActivityLogResponse(BaseModel):
    log_id: int
    user_id: int
    user_name: Optional[str] = None
    action: str
    entity: str
    entity_id: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True