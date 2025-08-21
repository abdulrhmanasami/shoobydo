from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Numeric, Index, CheckConstraint
from sqlalchemy.orm import relationship
from .models import Base
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    status = Column(String(32), nullable=False, default="pending")
    currency = Column(String(3), nullable=False, default="EUR")
    total = Column(Numeric(12,2), nullable=False, default=0)
    notes = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    customer = relationship("Customer")
    __table_args__ = (
        Index("ix_orders_customer_id", "customer_id"),
        Index("ix_orders_status", "status"),
        Index("ix_orders_created_at", "created_at"),
        CheckConstraint("total >= 0", name="ck_orders_total_nonneg"),
        CheckConstraint("length(currency)=3", name="ck_orders_currency_len3"),
    )
