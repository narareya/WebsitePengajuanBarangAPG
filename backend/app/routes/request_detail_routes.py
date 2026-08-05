from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.request_detail_schema import RequestDetailCreate, RequestDetailUpdate, RequestDetailResponse
from app.services import request_detail_service
from app.middlewares.auth_middleware import get_current_user

router = APIRouter(prefix="/request-details", tags=["Request Details"])

@router.post("/", response_model=RequestDetailResponse, status_code=201)
def add_detail(
    data: RequestDetailCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return request_detail_service.add_detail(db, data.request_id, data.product_id, data.quantity)

@router.get("/request/{request_id}", response_model=list[RequestDetailResponse])
def get_details_by_request(
    request_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return request_detail_service.get_details_by_request(db, request_id)

@router.get("/{detail_id}", response_model=RequestDetailResponse)
def get_detail(
    detail_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return request_detail_service.get_detail(db, detail_id)

@router.patch("/{detail_id}", response_model=RequestDetailResponse)
def update_detail(
    detail_id: int,
    data: RequestDetailUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    fields = data.model_dump(exclude_unset=True)
    detail = request_detail_service.update_detail(db, detail_id, fields)
    if detail is None:
        raise HTTPException(status_code=404, detail="Detail tidak ditemukan")
    return detail

@router.delete("/{detail_id}", status_code=204)
def delete_detail(
    detail_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = request_detail_service.delete_detail(db, detail_id)
    if not success:
        raise HTTPException(status_code=404, detail="Detail tidak ditemukan")