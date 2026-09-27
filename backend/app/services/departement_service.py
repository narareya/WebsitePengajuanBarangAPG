from sqlalchemy.orm import Session
from app.repositories import departement_repository
from app.services import activity_log_service
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def create_departement(db: Session, data, user_id: int):
    try:
        departement = departement_repository.insert_departement(
            db, data.departement_code, data.departement_name, data.departement_status
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Kode departement sudah dipakai")

    activity_log_service.log_activity(
        db, user_id, "create", "department", departement.departement_id, f"Membuat department {departement.departement_name}"
    )
    return departement


def get_all_departements(db: Session):
    return departement_repository.find_all(db)


def get_departement(db: Session, departement_id: int):
    return departement_repository.find_by_id(db, departement_id)


def update_departement(db: Session, departement_id: int, data, user_id: int):
    fields = data.model_dump(exclude_unset=True)
    departement = departement_repository.update(db, departement_id, fields)
    if departement is not None:
        activity_log_service.log_activity(
            db, user_id, "update", "department", departement_id, f"Mengubah department {departement.departement_name}"
        )
    return departement


def delete_departement(db: Session, departement_id: int, user_id: int):
    departement = departement_repository.find_by_id(db, departement_id)
    success = departement_repository.delete(db, departement_id)
    if success:
        activity_log_service.log_activity(
            db, user_id, "delete", "department", departement_id, f"Menghapus department {departement.departement_name if departement else departement_id}"
        )
    return success