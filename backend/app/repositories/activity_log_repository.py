from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog
from app.models.user import User


def create_log(db: Session, user_id: int, action: str, entity: str, entity_id: int = None, description: str = None):
    log = ActivityLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        description=description
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def _apply_filters(query, action=None, entity=None, search=None, start_date=None, end_date=None):
    if action:
        query = query.filter(ActivityLog.action == action)
    if entity:
        query = query.filter(ActivityLog.entity == entity)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))
    if start_date:
        query = query.filter(ActivityLog.created_at >= start_date)
    if end_date:
        query = query.filter(ActivityLog.created_at < end_date + timedelta(days=1))
    return query


def _attach_user_names(logs):
    for log in logs:
        log.user_name = log.user.name if log.user else None
    return logs


def find_filtered(db: Session, action: str = None, entity: str = None, search: str = None,
                   start_date=None, end_date=None, page: int = 1, limit: int = 10):
    query = db.query(ActivityLog).join(User, ActivityLog.user_id == User.user_id)
    query = _apply_filters(query, action, entity, search, start_date, end_date)

    total = query.count()
    logs = query.order_by(ActivityLog.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return {"items": _attach_user_names(logs), "total": total, "page": page, "limit": limit}


def find_all_filtered(db: Session, action: str = None, entity: str = None, search: str = None,
                       start_date=None, end_date=None):
    query = db.query(ActivityLog).join(User, ActivityLog.user_id == User.user_id)
    query = _apply_filters(query, action, entity, search, start_date, end_date)
    logs = query.order_by(ActivityLog.created_at.desc()).all()
    return _attach_user_names(logs)
