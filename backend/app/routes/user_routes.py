from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.update_user(db, user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")