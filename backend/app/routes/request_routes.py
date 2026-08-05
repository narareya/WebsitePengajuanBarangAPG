from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
from app.config.database import get_db
from app.schemas.request_schema import RequestCreate, RequestApprove, RequestResponse, RequestWithDetailsResponse
from app.services import request_service
from app.middlewares.auth_middleware import get_current_user, require_role

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("/", response_model=RequestWithDetailsResponse, status_code=201)
def create_request(
    data: RequestCreate,
    current_user=Depends(require_role("employee")),
    db: Session = Depends(get_db)
):
    items = [item.model_dump() for item in data.items]
    
    return request_service.create_request(db, current_user.user_id, items)


@router.get("/", response_model=dict)
def get_all_requests(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(require_role("manager", "admin")),
    db: Session = Depends(get_db)
):
    return request_service.get_all_requests_filtered(db, status, search, page, limit)


@router.get("/me", response_model=dict)
def get_my_requests(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return request_service.get_requests_by_user_filtered(db, current_user.user_id, status, page, limit)


@router.get("/{request_id}", response_model=RequestWithDetailsResponse)
def get_request(
    request_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return request_service.get_request_with_details(db, request_id)


@router.patch("/{request_id}/approve", response_model=RequestResponse)
def approve_request(
    request_id: int,
    data: RequestApprove,
    current_user=Depends(require_role("manager", "admin")),
    db: Session = Depends(get_db)
):
    return request_service.approve_request(db, request_id, current_user.user_id, data.status, data.reason)


@router.patch("/{request_id}/items", response_model=RequestWithDetailsResponse)
def update_request_items(
    request_id: int,
    data: RequestCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = [item.model_dump() for item in data.items]
    return request_service.update_request_items(db, request_id, current_user.user_id, items)


@router.delete("/{request_id}", status_code=204)
def delete_request(
    request_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = request_service.delete_request(db, request_id, current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Request tidak ditemukan")


@router.post("/{request_id}/attachment", response_model=RequestWithDetailsResponse)
async def upload_attachment(
    request_id: int,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_data = await file.read()
    request_service.upload_attachment(db, request_id, current_user.user_id, file.filename, file_data)
    return request_service.get_request_with_details(db, request_id)


@router.get("/{request_id}/attachment")
def download_attachment(
    request_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = request_service.download_attachment(db, request_id)
    return Response(
        content=result["data"],
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{result["filename"]}"'}
    )