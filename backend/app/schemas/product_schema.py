from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    product_code: str = Field(..., max_length=20)
    product_name: str = Field(..., max_length=100)
    product_desc: Optional[str] = Field(None, max_length=255)
    product_price: float = Field(..., gt=0)
    product_status: str = "active"
    stock_quantity: int = Field(0, ge=0)

class ProductUpdate(BaseModel):
    product_code: Optional[str] = Field(None, max_length=20)
    product_name: Optional[str] = Field(None, max_length=100)
    product_desc: Optional[str] = Field(None, max_length=255)
    product_price: Optional[float] = Field(None, gt=0)
    product_status: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)

class AddStock(BaseModel):
    quantity: int = Field(..., gt=0)

class ProductResponse(BaseModel):
    product_id: int
    product_code: str
    product_name: str
    product_desc: Optional[str] = None
    product_price: float
    product_status: str
    stock_quantity: int

    class Config:
        from_attributes = True