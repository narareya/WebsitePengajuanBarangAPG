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


def find_filtered(db: Session, action: str = None, search: str = None, page: int = 1, limit: int = 10):
    query = db.query(ActivityLog).join(User, ActivityLog.user_id == User.user_id)

    if action:
        query = query.filter(ActivityLog.action == action)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))

    total = query.count()
    logs = query.order_by(ActivityLog.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    results = []
    for log in logs:
        log.user_name = log.user.name if log.user else None
        results.append(log)

    return {"items": results, "total": total, "page": page, "limit": limit}