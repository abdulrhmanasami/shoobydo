"""
Stock Movement Model

Tracks all stock changes including reservations, releases, and manual adjustments.
Used for inventory management and audit trail.

Author: Cursor (auto-generated)
Purpose: Track stock movements for products
Last updated: 2025-08-21
"""

from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship
from .models import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    qty_change = Column(Integer, nullable=False)  # positive for additions, negative for reductions
    reason = Column(String(64), nullable=False)  # 'reserve', 'release', 'manual_adjust', 'purchase', 'sale'
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="stock_movements")
