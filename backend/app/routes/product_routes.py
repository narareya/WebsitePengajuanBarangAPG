from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)


@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get("/active", response_model=list[ProductResponse])
def get_active_products(db: Session = Depends(get_db)):
    return product_service.get_active_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = product_service.update_product(db, product_id, data)
    if product is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")