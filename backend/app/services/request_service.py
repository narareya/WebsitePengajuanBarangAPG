from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import request_repository, request_detail_repository, product_repository
from app.schemas.request_schema import RequestResponse
from app.services import activity_log_service

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def create_request(db: Session, user_id: int, items: list[dict]):
    if not items:
        raise HTTPException(status_code=400, detail="Request harus punya minimal 1 barang")

    for item in items:
        product = product_repository.find_by_id(db, item["product_id"])
        if product is None:
            raise HTTPException(status_code=404, detail=f"Produk id {item['product_id']} tidak ditemukan")

    request = request_repository.insert_request(db, user_id)
    request_detail_repository.insert_many_details(db, request.request_id, items)

    activity_log_service.log_activity(
        db, user_id, "create", "request", request.request_id, "Membuat pengajuan baru"
    )

    return get_request_with_details(db, request.request_id)


def get_all_requests_filtered(db: Session, status: str, search: str, page: int, limit: int):
    result = request_repository.find_filtered(db, status=status, search=search, page=page, limit=limit)
    return {
        "items": [RequestResponse.model_validate(r) for r in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"],
        "total_pages": (result["total"] + limit - 1) // limit if limit else 1
    }


def get_requests_by_user_filtered(db: Session, user_id: int, status: str, page: int, limit: int):
    result = request_repository.find_filtered(db, status=status, user_id=user_id, page=page, limit=limit)
    return {
        "items": [RequestResponse.model_validate(r) for r in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"],
        "total_pages": (result["total"] + limit - 1) // limit if limit else 1
    }


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
        "attachment_name": request.attachment_name,
        "details": details
    }


def approve_request(db: Session, request_id: int, approved_by: int, new_status: str):
    if new_status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status harus 'approved' atau 'rejected'")

    request = request_repository.find_by_id(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Request ini sudah diproses sebelumnya")

    result = request_repository.approve(db, request_id, approved_by, new_status)

    action = "approve" if new_status == "approved" else "reject"
    activity_log_service.log_activity(
        db, approved_by, action, "request", request_id, f"Pengajuan #{request_id} di-{new_status}"
    )

    return result


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

    request_detail_repository.delete_by_request(db, request_id)
    request_detail_repository.insert_many_details(db, request_id, items)

    activity_log_service.log_activity(
        db, user_id, "update", "request", request_id, "Mengubah barang pada pengajuan"
    )

    return get_request_with_details(db, request_id)


def delete_request(db: Session, request_id: int, user_id: int):
    request = request_repository.find_by_id(db, request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")

    if request.user_id != user_id:
        raise HTTPException(status_code=403, detail="Kamu tidak punya akses ke pengajuan ini")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Pengajuan yang sudah diproses tidak bisa dihapus")

    request_detail_repository.delete_by_request(db, request_id)
    result = request_repository.delete(db, request_id)

    activity_log_service.log_activity(
        db, user_id, "delete", "request", request_id, "Menghapus pengajuan"
    )

    return result


def upload_attachment(db: Session, request_id: int, user_id: int, filename: str, file_data: bytes):
    request = request_repository.find_by_id(db, request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")

    if request.user_id != user_id:
        raise HTTPException(status_code=403, detail="Kamu tidak punya akses ke pengajuan ini")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Lampiran hanya bisa diunggah saat status masih pending")

    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Ukuran file maksimal 5MB")

    result = request_repository.save_attachment(db, request_id, filename, file_data)

    activity_log_service.log_activity(
        db, user_id, "update", "request", request_id, f"Mengunggah lampiran: {filename}"
    )

    return result


def download_attachment(db: Session, request_id: int):
    result = request_repository.get_attachment(db, request_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Lampiran tidak ditemukan")
    return result