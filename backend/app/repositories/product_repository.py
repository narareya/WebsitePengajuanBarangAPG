from sqlalchemy.orm import Session
from app.models.product import Product

def find_all(db: Session):
    return db.query(Product).all()

def find_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()

def find_by_status(db: Session, product_status: str):
    return db.query(Product).filter(Product.product_status == product_status).all()

def insert_product(db: Session, product_code: str, product_name: str, product_desc: str, product_price: float, product_status: str = "active"):
    product = Product(
        product_code=product_code,
        product_name=product_name,
        product_desc=product_desc,
        product_price=product_price,
        product_status=product_status
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update(db: Session, product_id: int, fields: dict):
    product = find_by_id(db, product_id)
    if product is None:
        return None
    for key, value in fields.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete(db: Session, product_id: int):
    product = find_by_id(db, product_id)
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True