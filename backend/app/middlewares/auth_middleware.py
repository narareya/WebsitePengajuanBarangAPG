from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.config.database import get_db
from app.utils.security import decode_access_token
from app.repositories import user_repository, token_blacklist_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token tidak valid atau sudah kadaluarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token_blacklist_repository.is_blacklisted(db, token):
        raise HTTPException(
            status_code=401,
            detail="Token sudah tidak berlaku, silakan login kembali",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_repository.find_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user


def require_role(*allowed_roles: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Kamu tidak punya akses ke fitur ini")
        return current_user
    return role_checker