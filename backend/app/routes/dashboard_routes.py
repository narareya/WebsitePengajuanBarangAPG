from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.request import RequestModel
from app.models.product import Product
from app.models.user import User
from app.schemas.dashboard_schema import DashboardSummary, RecentActivityItem, LowStockProduct
from app.middlewares.auth_middleware import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

STATUS_LABELS = {
    "approved": "Disetujui",
    "pending": "Menunggu",
    "rejected": "Ditolak",
}

LOW_STOCK_THRESHOLD = 5


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(RequestModel)

    if current_user.role == "employee":
        query = query.filter(RequestModel.user_id == current_user.user_id)

    total = query.count()
    pending = query.filter(RequestModel.status == "pending").count()
    approved_total = query.filter(RequestModel.status == "approved").count()

    status_counts = (
        query.with_entities(RequestModel.status, func.count(RequestModel.request_id))
        .group_by(RequestModel.status)
        .all()
    )
    by_status = {status: count for status, count in status_counts}

    now = datetime.utcnow()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_end = this_month_start - timedelta(seconds=1)
    last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    this_month_count = query.filter(RequestModel.request_date >= this_month_start).count()
    last_month_count = query.filter(
        RequestModel.request_date >= last_month_start,
        RequestModel.request_date <= last_month_end,
    ).count()

    total_trend = None
    if last_month_count > 0:
        total_trend = round(
            ((this_month_count - last_month_count) / last_month_count) * 100, 1
        )

    low_stock_count = 0
    low_stock_products = []
    if current_user.role in ("admin", "manager"):
        low_stock_products_query = (
            db.query(Product)
            .filter(Product.stock_quantity <= LOW_STOCK_THRESHOLD)
            .order_by(Product.stock_quantity.asc())
        )
        low_stock_count = low_stock_products_query.count()
        low_stock_products = [
            LowStockProduct(product_id=p.product_id, product_name=p.product_name, stock_quantity=p.stock_quantity)
            for p in low_stock_products_query.limit(8).all()
        ]

    return DashboardSummary(
        total_submissions=approved_total if current_user.role == "manager" else total,
        pending_approval=pending,
        total_trend=total_trend,
        by_status=by_status,
        low_stock_count=low_stock_count,
        low_stock_products=low_stock_products,
    )


@router.get("/recent-activity", response_model=list[RecentActivityItem])
def get_recent_activity(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(RequestModel).join(User, RequestModel.user_id == User.user_id)

    if current_user.role == "employee":
        query = query.filter(RequestModel.user_id == current_user.user_id)

    rows = (
        query.order_by(RequestModel.request_date.desc())
        .limit(limit)
        .with_entities(
            RequestModel.request_id,
            User.name.label("actor"),
            RequestModel.status,
            RequestModel.request_date,
        )
        .all()
    )

    return [
        RecentActivityItem(
            id=row.request_id,
            title=f"Request #{row.request_id}",
            actor=row.actor,
            status=row.status,
            status_label=STATUS_LABELS.get(row.status, row.status.capitalize()),
            created_at=row.request_date,
        )
        for row in rows
    ]