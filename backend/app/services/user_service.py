from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories import user_repository
from app.services import activity_log_service
from app.utils.security import hash_password
from fastapi import HTTPException


def create_user(db: Session, data, actor_id: int):
    hashed = hash_password(data.password)
    try:
        user = user_repository.insert_user(
            db, data.name, data.email, hashed, data.role.value, data.departement_id, data.user_status.value
        )
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e.orig):
            raise HTTPException(status_code=409, detail="Email sudah terdaftar")
        raise HTTPException(status_code=400, detail="Department tidak ditemukan")

    activity_log_service.log_activity(
        db, actor_id, "create", "user", user.user_id, f"Membuat user {user.name}"
    )
    return user


def get_all_users(db: Session):
    return user_repository.find_all(db)


def get_user(db: Session, user_id: int):
    return user_repository.find_by_id(db, user_id)


def update_user(db: Session, user_id: int, data, actor_id: int):
    fields = data.model_dump(exclude_unset=True)

    if "password" in fields:
        fields["password"] = hash_password(fields["password"])
    if "role" in fields:
        fields["role"] = fields["role"].value
    if "user_status" in fields:
        fields["user_status"] = fields["user_status"].value

    user = user_repository.update(db, user_id, fields)
    if user is not None:
        activity_log_service.log_activity(
            db, actor_id, "update", "user", user_id, f"Mengubah user {user.name}"
        )
    return user


def delete_user(db: Session, user_id: int, actor_id: int):
    user = user_repository.find_by_id(db, user_id)
    success = user_repository.delete(db, user_id)
    if success:
        activity_log_service.log_activity(
            db, actor_id, "delete", "user", user_id, f"Menghapus user {user.name if user else user_id}"
        )
    return success