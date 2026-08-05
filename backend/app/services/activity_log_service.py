from sqlalchemy.orm import Session
from app.repositories import activity_log_repository


def log_activity(db: Session, user_id: int, action: str, entity: str, entity_id: int = None, description: str = None):
    return activity_log_repository.create_log(db, user_id, action, entity, entity_id, description)


def get_logs(db: Session, action, search, page, limit):
    result = activity_log_repository.find_filtered(db, action=action, search=search, page=page, limit=limit)
    return {
        "items": result["items"],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"],
        "total_pages": (result["total"] + limit - 1) // limit
    }