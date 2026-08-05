from sqlalchemy import String
from sqlalchemy.orm import Session
from app.models.request import RequestModel
from app.models.user import User
from datetime import datetime

def find_all(db: Session):
    return db.query(RequestModel).all()

def find_by_id(db: Session, request_id: int):
    return db.query(RequestModel).filter(RequestModel.request_id == request_id).first()

def find_by_status(db: Session, request_status: str):
    return db.query(RequestModel).filter(RequestModel.status == request_status).all()

def find_by_user(db: Session, user_id: int):
    return db.query(RequestModel).filter(RequestModel.user_id == user_id).all()

def insert_request(db: Session, user_id: int):
    request = RequestModel(
        user_id=user_id,
        status="pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def update(db:Session, request_id:int, fields: dict):
    request = find_by_id(db, request_id)
    if request is None:
        return None
    for key, value in fields.items():
        setattr(request, key, value)
    db.commit()
    db.refresh(request)
    return request

def delete(db: Session, request_id: int):
    request = find_by_id(db, request_id)
    if request is None:
        return False
    db.delete(request)
    db.commit()
    return True

def find_filtered(db: Session, status: str = None, search: str = None, user_id: int = None, page: int = 1, limit: int = 10):
    query = db.query(RequestModel)

    if user_id is not None:
        query = query.filter(RequestModel.user_id == user_id)
    if status:
        query = query.filter(RequestModel.status == status)
    if search:
        query = query.join(User, RequestModel.user_id == User.user_id).filter(
            (User.name.ilike(f"%{search}%")) | (RequestModel.request_id.cast(String).ilike(f"%{search}%"))
        )

    total = query.count()
    items = query.order_by(RequestModel.request_date.desc()).offset((page - 1) * limit).limit(limit).all()

    return {"items": items, "total": total, "page": page, "limit": limit}


def approve(db: Session, request_id: int, approved_by: int, new_status: str):
    request = find_by_id(db, request_id)
    if request is None:
        return None
    request.status = new_status
    request.approved_by = approved_by
    request.approved_at = datetime.utcnow()

    db.commit()
    db.refresh(request)
    return request