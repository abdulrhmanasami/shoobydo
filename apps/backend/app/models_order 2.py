from sqlalchemy import Column, Integer, String, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from .models import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String(255), nullable=False, index=True)
    status = Column(String(32), nullable=False, default="new", index=True)
    total = Column(Numeric(12,2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
