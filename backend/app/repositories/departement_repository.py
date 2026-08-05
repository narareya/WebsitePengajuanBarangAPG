from sqlalchemy.orm import Session
from app.models.departement import Departement

def find_all(db: Session):
    return db.query(Departement).all()


def find_by_id(db: Session, departement_id: int):
    return db.query(Departement).filter(Departement.departement_id == departement_id).first()


def insert_departement(db: Session, code: str, name: str, status: str):
    department = Departement(
        departement_code=code,
        departement_name=name,
        departement_status=status
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


def update(db: Session, departement_id: int, fields: dict):
    department = find_by_id(db, departement_id)
    if department is None:
        return None
    for key, value in fields.items():
        setattr(department, key, value)
    db.commit()
    db.refresh(department)
    return department


def delete(db: Session, departement_id: int):
    department = find_by_id(db, departement_id)
    if department is None:
        return False
    db.delete(department)
    db.commit()
    return True