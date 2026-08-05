from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import request_detail_repository, product_repository, request_repository

def get_details_by_request(db: Session, request_id: int):
    return request_detail_repository.find_by_request(db, request_id)

def get_detail(db: Session, detail_id: int):
    detail = request_detail_repository.find_by_id(db, detail_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Detail tidak ditemukan")
    return detail

def add_detail(db: Session, request_id: int, product_id: int, quantity: int):
    request = request_repository.find_by_id(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Tidak bisa menambah barang, request sudah diproses")

    product = product_repository.find_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Jumlah barang harus lebih dari 0")

    return request_detail_repository.insert_detail(db, request_id, product_id, quantity)

def update_detail(db: Session, detail_id: int, fields: dict):
    if "quantity" in fields and fields["quantity"] <= 0:
        raise HTTPException(status_code=400, detail="Jumlah barang harus lebih dari 0")
    return request_detail_repository.update(db, detail_id, fields)

def delete_detail(db: Session, detail_id: int):
    return request_detail_repository.delete(db, detail_id)