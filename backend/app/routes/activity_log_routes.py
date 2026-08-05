from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.config.database import get_db
from app.schemas.activity_log_schema import ActivityLogResponse
from app.services import activity_log_service
from app.middlewares.auth_middleware import require_role

router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


@router.get("/", response_model=dict)
def get_activity_logs(
    action: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    result = activity_log_service.get_logs(db, action, search, page, limit)
    result["items"] = [ActivityLogResponse.model_validate(log) for log in result["items"]]
    return result