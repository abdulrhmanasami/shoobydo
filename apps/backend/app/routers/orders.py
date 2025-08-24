from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, and_, desc
from typing import Dict, Any
from datetime import datetime, date
from app.db import get_db
from app.security import get_current_user, require_role
from app.models_order import Order
from app.models_customer import Customer
from app.models_order_item import OrderItem
from app.schemas_order import OrderCreate, OrderUpdate, OrderOut
router = APIRouter(prefix="/orders", tags=["orders"])
@router.get("/", response_model=list[OrderOut])
def list_orders(
    q: str | None = Query(default=None),
    status: str | None = Query(default=None),
    customer_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user=Depends(require_user),
):
    qs = db.query(Order)
    if q:
        like = f"%{q}%"
        qs = qs.filter(or_(Order.status.ilike(like), Order.currency.ilike(like), Order.notes.ilike(like)))
    if status:
        qs = qs.filter(Order.status == status)
    if customer_id:
        qs = qs.filter(Order.customer_id == customer_id)
    return qs.order_by(Order.id.desc()).offset(offset).limit(limit).all()

@router.get("/{oid}", response_model=OrderOut)
def get_order(oid: int = Path(..., ge=1), db: Session = Depends(get_db), user=Depends(require_user)):
    obj = db.get(Order, oid)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    return obj
@router.post("/", response_model=OrderOut, dependencies=[Depends(require_any_role("admin","manager"))])
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    if not db.get(Customer, data.customer_id):
        raise HTTPException(status_code=422, detail="customer not found")
    obj = Order(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
@router.put("/{oid}", response_model=OrderOut, dependencies=[Depends(require_any_role("admin","manager"))])
def update_order(oid: int, data: OrderUpdate, db: Session = Depends(get_db)):
    obj = db.get(Order, oid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    patch = data.model_dump(exclude_none=True)
    if "customer_id" in patch and not db.get(Customer, patch["customer_id"]):
        raise HTTPException(status_code=422, detail="customer not found")
    for k,v in patch.items(): setattr(obj, k, v)
    db.commit(); db.refresh(obj); return obj
@router.delete("/{oid}", dependencies=[Depends(require_any_role("admin"))])
def delete_order(oid: int, db: Session = Depends(get_db)):
    obj = db.get(Order, oid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    db.delete(obj); db.commit(); return {"ok": True}

# Advanced Order Management Features

@router.get("/stats/summary")
def get_orders_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(require_user)
) -> Dict[str, Any]:
    """Get orders summary statistics"""
    query = db.query(Order)
    
    if start_date:
        query = query.filter(func.date(Order.created_at) >= start_date)
    if end_date:
        query = query.filter(func.date(Order.created_at) <= end_date)
    
    total_orders = query.count()
    total_revenue = query.with_entities(func.sum(Order.total)).scalar() or 0
    
    # Status breakdown
    status_counts = (
        query.with_entities(Order.status, func.count(Order.id))
        .group_by(Order.status)
        .all()
    )
    
    # Currency breakdown
    currency_totals = (
        query.with_entities(Order.currency, func.sum(Order.total))
        .group_by(Order.currency)
        .all()
    )
    
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "status_breakdown": {status: count for status, count in status_counts},
        "currency_breakdown": {currency: float(total) for currency, total in currency_totals},
        "period": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }
    }

@router.get("/stats/daily")
def get_daily_orders_stats(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
    user=Depends(require_user)
) -> Dict[str, Any]:
    """Get daily orders statistics for the last N days"""
    from datetime import timedelta
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    daily_stats = (
        db.query(
            func.date(Order.created_at).label('date'),
            func.count(Order.id).label('count'),
            func.sum(Order.total).label('revenue')
        )
        .filter(func.date(Order.created_at) >= start_date)
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
        .all()
    )
    
    return {
        "period": {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
        "daily_stats": [
            {
                "date": stat.date.isoformat(),
                "orders_count": stat.count,
                "revenue": float(stat.revenue or 0)
            }
            for stat in daily_stats
        ]
    }

@router.get("/customer/{customer_id}/orders", response_model=list[OrderOut])
def get_customer_orders(
    customer_id: int = Path(..., ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    """Get all orders for a specific customer"""
    # Verify customer exists
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(desc(Order.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    return orders

@router.post("/{oid}/status")
def update_order_status(
    oid: int = Path(..., ge=1),
    new_status: str = Query(...),
    notes: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(require_any_role("admin", "manager"))
) -> Dict[str, Any]:
    """Update order status with optional notes"""
    valid_statuses = ["pending", "paid", "cancelled", "refunded"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=422, 
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    order = db.get(Order, oid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    old_status = order.status
    order.status = new_status
    
    if notes:
        order.notes = f"{order.notes or ''}\n[{datetime.now().isoformat()}] Status changed from {old_status} to {new_status}: {notes}".strip()
    
    db.commit()
    db.refresh(order)
    
    return {
        "order_id": oid,
        "old_status": old_status,
        "new_status": new_status,
        "updated_at": order.updated_at.isoformat() if order.updated_at else None
    }

@router.get("/{oid}/items-summary")
def get_order_items_summary(
    oid: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    user=Depends(require_user)
) -> Dict[str, Any]:
    """Get summary of items in an order"""
    order = db.get(Order, oid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items_stats = (
        db.query(
            func.count(OrderItem.id).label('total_items'),
            func.sum(OrderItem.qty).label('total_quantity'),
            func.sum(OrderItem.subtotal).label('total_amount')
        )
        .filter(OrderItem.order_id == oid)
        .first()
    )
    
    return {
        "order_id": oid,
        "total_items": items_stats.total_items or 0,
        "total_quantity": items_stats.total_quantity or 0,
        "total_amount": float(items_stats.total_amount or 0),
        "order_total": float(order.total)
    }
