from sqlalchemy.orm import Session
from app.models.request_detail import RequestDetail

def find_all(db: Session):
    return db.query(RequestDetail).all()

def find_by_id(db: Session, detail_id: int):
    return db.query(RequestDetail).filter(RequestDetail.detail_id == detail_id).first()

def find_by_request(db: Session, request_id: int):
    details = db.query(RequestDetail).filter(RequestDetail.request_id == request_id).all()
    for d in details: 
        d.product_name = d.product.product_name if d.product else None
    return details


def insert_detail(db: Session, request_id: int, product_id: int, quantity: int):
    detail = RequestDetail(
        request_id=request_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail

def insert_many_details(db: Session, request_id: int, items: list[dict]):
    details = [
        RequestDetail(request_id=request_id, product_id=item["product_id"], quantity=item["quantity"])
        for item in items
    ]
    db.add_all(details)
    db.commit()
    for detail in details:
        db.refresh(detail)
    return details

def update(db: Session, detail_id: int, fields: dict):
    detail = find_by_id(db, detail_id)
    if detail is None:
        return None
    for key, value in fields.items():
        setattr(detail, key, value)
    db.commit()
    db.refresh(detail)
    return detail

def delete(db: Session, detail_id: int):
    detail = find_by_id(db, detail_id)
    if detail is None:
        return False
    db.delete(detail)
    db.commit()
    return True

def delete_by_request(db: Session, request_id: int):
    db.query(RequestDetail).filter(RequestDetail.request_id == request_id).delete()
    db.commit()
    return True