from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models_order import Order
from app.models_order_item import OrderItem

def recalc_order_total(db: Session, order_id: int) -> None:
    total = db.query(func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0)).filter(
        OrderItem.order_id == order_id
    ).scalar()
    ord = db.get(Order, order_id)
    if ord is not None:
        ord.total = total
        db.commit()
        db.refresh(ord)
