from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import request_repository, request_detail_repository, product_repository

def create_request(db: Session, user_id: int, items: list[dict]):
    if not items:
        raise HTTPException(status_code=400, detail="Request harus punya minimal 1 barang")

    for item in items:
        product = product_repository.find_by_id(db, item["product_id"])
        if product is None:
            raise HTTPException(status_code=404, detail=f"Produk id {item['product_id']} tidak ditemukan")

    request = request_repository.insert_request(db, user_id)

    request_detail_repository.insert_many_details(db, request.request_id, items)

    return get_request_with_details(db, request.request_id)

def get_all_requests(db: Session):
    return request_repository.find_all(db)

def get_request(db: Session, request_id: int):
    request = request_repository.find_by_id(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")
    return request

def get_request_with_details(db: Session, request_id: int):
    request = get_request(db, request_id)
    details = request_detail_repository.find_by_request(db, request_id)
    return {
        "request_id": request.request_id,
        "user_id": request.user_id,
        "request_date": request.request_date,
        "status": request.status,
        "approved_by": request.approved_by,
        "approved_at": request.approved_at,
        "details": details
    }

def get_requests_by_user(db: Session, user_id: int):
    return request_repository.find_by_user(db, user_id)

def get_requests_by_status(db: Session, status: str):
    return request_repository.find_by_status(db, status)

def approve_request(db: Session, request_id: int, approved_by: int, new_status: str):
    if new_status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status harus 'approved' atau 'rejected'")

    request = request_repository.find_by_id(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Request ini sudah diproses sebelumnya")

    return request_repository.approve(db, request_id, approved_by, new_status)

def delete_request(db: Session, request_id: int):
    from app.repositories import request_detail_repository
    request_detail_repository.delete_by_request(db, request_id)
    return request_repository.delete(db, request_id)

def update_request_items(db: Session, request_id: int, user_id: int, items: list[dict]):
    request = request_repository.find_by_id(db, request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")

    if request.user_id != user_id:
        raise HTTPException(status_code=403, detail="Kamu tidak punya akses ke pengajuan ini")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Pengajuan yang sudah diproses tidak bisa diedit")

    if not items:
        raise HTTPException(status_code=400, detail="Request harus punya minimal 1 barang")

    for item in items:
        product = product_repository.find_by_id(db, item["product_id"])
        if product is None:
            raise HTTPException(status_code=404, detail=f"Produk id {item['product_id']} tidak ditemukan")

    # hapus semua detail lama, ganti dengan yang baru
    request_detail_repository.delete_by_request(db, request_id)
    request_detail_repository.insert_many_details(db, request_id, items)

    return get_request_with_details(db, request_id)