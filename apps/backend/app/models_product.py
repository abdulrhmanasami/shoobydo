from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .models import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    price = Column(Numeric(12,2), nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)  # legacy field
    stock_on_hand = Column(Integer, nullable=False, default=0)  # actual available stock
    stock_reserved = Column(Integer, nullable=False, default=0)  # reserved for orders
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    stock_movements = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")
