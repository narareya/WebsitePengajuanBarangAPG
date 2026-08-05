from sqlalchemy.orm import Session
from app.models.user import User

def find_all(db: Session):
    return db.query(User).all()

def find_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def find_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def insert_user(db: Session, name: str, email: str, hashed_password: str, role: str, departement_id: int, user_status: str):
    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role,
        departement_id=departement_id,
        user_status=user_status
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update(db: Session, user_id: int, fields: dict):
    user = find_by_id(db, user_id)
    if user is None:
        return None
    for key, value in fields.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete(db: Session, user_id: int):
    user = find_by_id(db, user_id)
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True