from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class RequestDetail(Base):
    __tablename__ = "request_detail"

    detail_id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.request_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    request = relationship("RequestModel", back_populates="details")
    product = relationship("Product")