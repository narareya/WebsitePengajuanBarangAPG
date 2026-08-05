from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database import Base

class RequestModel(Base):
    __tablename__ = "requests"

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    request_date = Column(DateTime, server_default=func.now())
    status = Column(String(20), nullable=False, default="pending")
    approved_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="requests", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approved_by])
    details = relationship("RequestDetail", back_populates="request")