from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse, AddStock
from app.services import product_service
from app.middlewares.auth_middleware import get_current_user, require_role

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    return product_service.create_product(db, data, current_user.user_id)


@router.get("/", response_model=list[ProductResponse])
def get_all_products(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.get("/active", response_model=list[ProductResponse])
def get_active_products(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return product_service.get_active_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    product = product_service.update_product(db, product_id, data, current_user.user_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product


@router.patch("/{product_id}/add-stock", response_model=ProductResponse)
def add_stock(
    product_id: int,
    data: AddStock,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    product = product_service.add_stock(db, product_id, data.quantity, current_user.user_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    success = product_service.delete_product(db, product_id, current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")