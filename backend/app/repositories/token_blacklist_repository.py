from sqlalchemy.orm import Session
from datetime import datetime
from app.models.token_blacklist import TokenBlacklist

def add(db: Session, token: str, expires_at):
    entry = TokenBlacklist(token=token, expires_at=datetime.utcfromtimestamp(expires_at))
    db.add(entry)
    db.commit()
    return entry

def is_blacklisted(db: Session, token: str) -> bool:
    return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None