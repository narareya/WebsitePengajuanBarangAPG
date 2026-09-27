from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories import product_repository
from app.services import activity_log_service
from fastapi import HTTPException

def add_stock(db: Session, product_id: int, quantity: int, user_id: int):
    product = product_repository.find_by_id(db, product_id)
    if product is None:
        return None

    old_stock = product.stock_quantity
    product = product_repository.increment_stock(db, product_id, quantity)

    activity_log_service.log_activity(
        db, user_id, "update", "product", product_id,
        f"Menambah stok {product.product_name} sebanyak +{quantity} (dari {old_stock} jadi {product.stock_quantity})"
    )
    return product

def create_product(db: Session, data, user_id: int):
    try:
        product = product_repository.insert_product(
            db,
            data.product_code,
            data.product_name,
            data.product_desc,
            data.product_price,
            data.product_status,
            data.stock_quantity
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Kode produk sudah dipakai")

    activity_log_service.log_activity(
        db, user_id, "create", "product", product.product_id, f"Membuat produk {product.product_name}"
    )
    return product

def get_all_products(db: Session):
    return product_repository.find_all(db)

def get_active_products(db: Session):
    return product_repository.find_by_status(db, "active")

def get_product(db: Session, product_id: int):
    return product_repository.find_by_id(db, product_id)

def update_product(db: Session, product_id: int, data, user_id: int):
    fields = data.model_dump(exclude_unset=True)
    product = product_repository.update(db, product_id, fields)
    if product is not None:
        activity_log_service.log_activity(
            db, user_id, "update", "product", product_id, f"Mengubah produk {product.product_name}"
        )
    return product

def delete_product(db: Session, product_id: int, user_id: int):
    product = product_repository.find_by_id(db, product_id)
    success = product_repository.delete(db, product_id)
    if success:
        activity_log_service.log_activity(
            db, user_id, "delete", "product", product_id, f"Menghapus produk {product.product_name if product else product_id}"
        )
    return success