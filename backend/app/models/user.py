from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    departement_id = Column(Integer, ForeignKey("departements.departement_id"), nullable=False)
    user_status = Column(String(20), nullable=False, default="active")

    department = relationship("Departement")
    requests = relationship("RequestModel", back_populates="user", foreign_keys="RequestModel.user_id"
    )