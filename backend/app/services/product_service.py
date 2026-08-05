from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories import product_repository
from fastapi import HTTPException

def create_product(db: Session, data):
    try:
        return product_repository.insert_product(
            db,
            data.product_code,
            data.product_name,
            data.product_desc,
            data.product_price,
            data.product_status
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Kode produk sudah dipakai")

def get_all_products(db: Session):
    return product_repository.find_all(db)

def get_active_products(db: Session):
    return product_repository.find_by_status(db, "active")

def get_product(db: Session, product_id: int):
    return product_repository.find_by_id(db, product_id)

def update_product(db: Session, product_id: int, data):
    fields = data.model_dump(exclude_unset=True)
    return product_repository.update(db, product_id, fields)

def delete_product(db: Session, product_id: int):
    return product_repository.delete(db, product_id)