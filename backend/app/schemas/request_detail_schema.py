from pydantic import BaseModel, Field
from typing import Optional

class RequestDetailItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class RequestDetailCreate(BaseModel):
    request_id: int
    product_id: int
    quantity: int = Field(..., gt=0)

class RequestDetailUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = Field(None, gt=0)

class RequestDetailResponse(BaseModel):
    detail_id: int
    request_id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None

    class Config:
        from_attributes = True