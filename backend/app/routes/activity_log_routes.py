from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.config.database import get_db
from app.schemas.activity_log_schema import ActivityLogResponse
from app.services import activity_log_service
from app.middlewares.auth_middleware import require_role
from app.utils.csv_export import build_csv_response

router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


@router.get("/", response_model=dict)
def get_activity_logs(
    action: Optional[str] = Query(None),
    entity: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    result = activity_log_service.get_logs(db, action, entity, search, start_date, end_date, page, limit)
    result["items"] = [ActivityLogResponse.model_validate(log) for log in result["items"]]
    return result


@router.get("/export")
def export_activity_logs(
    action: Optional[str] = Query(None),
    entity: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    logs = activity_log_service.get_logs_for_export(db, action, entity, search, start_date, end_date)
    rows = [
        [log.log_id, log.created_at.strftime("%Y-%m-%d %H:%M:%S"), log.user_name, log.action, log.entity, log.description]
        for log in logs
    ]
    return build_csv_response(
        "activity_log.csv",
        ["ID", "Waktu", "User", "Aksi", "Entity", "Keterangan"],
        rows
    )
