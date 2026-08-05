from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.config.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_code = Column(String(20), nullable=False)
    product_name = Column(String(100), nullable=False)
    product_desc = Column(String(255), nullable=True)
    product_price = Column(Numeric(12, 2), nullable=False)
    product_status = Column(String(20), nullable=False)

    request_details = relationship("RequestDetail", back_populates="product")