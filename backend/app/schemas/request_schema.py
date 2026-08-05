from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.request_detail_schema import RequestDetailItem, RequestDetailResponse


class RequestCreate(BaseModel):
    items: List[RequestDetailItem] = Field(..., min_length=1)

class RequestApprove(BaseModel):
    status: str
    reason: Optional[str] = None

class RequestResponse(BaseModel):
    request_id: int
    user_id: int
    user_name: Optional[str] = None
    request_date: datetime
    status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    attachment_name: Optional[str] = None

    class Config:
        from_attributes = True

class RequestWithDetailsResponse(BaseModel):
    request_id: int
    user_id: int
    request_date: datetime
    status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    attachment_name: Optional[str] = None
    details: List[RequestDetailResponse]

    class Config:
        from_attributes = True