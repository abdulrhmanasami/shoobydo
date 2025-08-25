from __future__ import annotations
from sqlalchemy import Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    supplier_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12,2), nullable=False, default=0)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # legacy field
    stock_on_hand: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # actual available stock
    stock_reserved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # reserved for orders
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    stock_movements: Mapped[list["StockMovement"]] = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")
