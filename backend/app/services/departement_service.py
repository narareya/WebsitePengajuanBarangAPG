from sqlalchemy.orm import Session
from app.repositories import departement_repository
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def create_departement(db: Session, data):
    try:
        return departement_repository.insert_departement(
            db, data.departement_code, data.departement_name, data.departement_status
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Kode departement sudah dipakai")


def get_all_departements(db: Session):
    return departement_repository.find_all(db)


def get_departement(db: Session, departement_id: int):
    return departement_repository.find_by_id(db, departement_id)


def update_departement(db: Session, departement_id: int, data):
    fields = data.model_dump(exclude_unset=True)
    return departement_repository.update(db, departement_id, fields)


def delete_departement(db: Session, departement_id: int):
    return departement_repository.delete(db, departement_id)