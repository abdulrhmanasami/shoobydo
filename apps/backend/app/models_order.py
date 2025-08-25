from __future__ import annotations
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Numeric, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")
    total: Mapped[float] = mapped_column(Numeric(12,2), nullable=False, default=0)
    notes: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    customer: Mapped["Customer"] = relationship("Customer")
    
    __table_args__ = (
        Index("ix_orders_customer_id", "customer_id"),
        Index("ix_orders_status", "status"),
        Index("ix_orders_created_at", "created_at"),
        CheckConstraint("total >= 0", name="ck_orders_total_nonneg"),
        CheckConstraint("length(currency)=3", name="ck_orders_currency_len3"),
    )
