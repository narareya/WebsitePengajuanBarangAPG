from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Departement(Base):
    __tablename__ = "departements"

    departement_id = Column(Integer, primary_key=True, index=True)
    departement_code = Column(String(20), nullable=False)
    departement_name = Column(String(100), nullable=False)
    departement_status = Column(String(20), nullable=False, default="active")