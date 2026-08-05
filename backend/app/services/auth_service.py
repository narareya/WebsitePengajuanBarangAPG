from sqlalchemy.orm import Session
from app.repositories import user_repository, token_blacklist_repository
from app.utils.security import verify_password, create_access_token, decode_access_token
from fastapi import HTTPException

def login(db: Session, data):
    user = user_repository.find_by_email(db, data.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Email atau password salah")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    if user.user_status != "active":
        raise HTTPException(status_code=403, detail="Akun tidak aktif")
    
    token = create_access_token({
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

def logout(db: Session, token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token tidak valid atau sudah expired")

    if token_blacklist_repository.is_blacklisted(db, token):
        raise HTTPException(status_code=401, detail="Token sudah tidak berlaku")

    token_blacklist_repository.add(db, token=token, expires_at=payload["exp"])

    return {"message": "Logout berhasil"}