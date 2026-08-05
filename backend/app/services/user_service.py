from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories import user_repository
from app.utils.security import hash_password
from fastapi import HTTPException


def create_user(db: Session, data):
    hashed = hash_password(data.password)
    try:
        return user_repository.insert_user(
            db, data.name, data.email, hashed, data.role.value, data.departement_id, data.user_status.value
        )
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e.orig):
            raise HTTPException(status_code=409, detail="Email sudah terdaftar")
        raise HTTPException(status_code=400, detail="Department tidak ditemukan")


def get_all_users(db: Session):
    return user_repository.find_all(db)


def get_user(db: Session, user_id: int):
    return user_repository.find_by_id(db, user_id)


def update_user(db: Session, user_id: int, data):
    fields = data.model_dump(exclude_unset=True)

    if "password" in fields:
        fields["password"] = hash_password(fields["password"])
    if "role" in fields:
        fields["role"] = fields["role"].value
    if "user_status" in fields:
        fields["user_status"] = fields["user_status"].value

    return user_repository.update(db, user_id, fields)


def delete_user(db: Session, user_id: int):
    return user_repository.delete(db, user_id)