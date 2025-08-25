"""
Stock Movement Model

Tracks all stock changes including reservations, releases, and manual adjustments.
Used for inventory management and audit trail.

Author: Cursor (auto-generated)
Purpose: Track stock movements for products
Last updated: 2025-08-24
"""

from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    qty_change: Mapped[int] = mapped_column(Integer, nullable=False)  # positive for additions, negative for reductions
    reason: Mapped[str] = mapped_column(String(64), nullable=False)  # 'reserve', 'release', 'manual_adjust', 'purchase', 'sale'
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="stock_movements")
