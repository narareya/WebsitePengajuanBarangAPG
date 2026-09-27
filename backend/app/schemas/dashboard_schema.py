from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel


class LowStockProduct(BaseModel):
    product_id: int
    product_name: str
    stock_quantity: int


class DashboardSummary(BaseModel):
    total_submissions: int
    pending_approval: int
    total_trend: Optional[float] = None
    by_status: Dict[str, int]
    low_stock_count: int = 0
    low_stock_products: List[LowStockProduct] = []


class RecentActivityItem(BaseModel):
    id: int
    title: str
    actor: str
    status: str
    status_label: str
    created_at: datetime

    class Config:
        from_attributes = True