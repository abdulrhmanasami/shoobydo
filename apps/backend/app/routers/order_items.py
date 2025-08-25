from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.db import get_db
from app.security import get_current_user, require_role
from app.models_order import Order
from app.models_product import Product
from app.models_order_item import OrderItem
from app.services.orders_total import recalc_order_total
from app.services.inventory import reserve_stock, release_stock
from app.schemas_order_item import OrderItemCreate, OrderItemUpdate, OrderItemOut

router = APIRouter(prefix="/orders", tags=["orders"])

def _recalc_total(db: Session, order_id: int):
    total = db.query(func.coalesce(func.sum(OrderItem.subtotal), 0)).filter(OrderItem.order_id==order_id).scalar()
    o = db.get(Order, order_id)
    if o:
        o.total = total
        db.commit()
        db.refresh(o)
    return total

@router.get("/{oid}/items", response_model=list[OrderItemOut])
def list_items(oid: int = Path(..., ge=1), db: Session = Depends(get_db), user=Depends(require_role)):
    if not db.get(Order, oid):
        raise HTTPException(status_code=404, detail="order not found")
    return db.query(OrderItem).filter_by(order_id=oid).order_by(OrderItem.id.desc()).all()

@router.post("/{oid}/items", response_model=OrderItemOut, dependencies=[Depends(require_role("admin"))])
def add_item(oid: int, data: OrderItemCreate, db: Session = Depends(get_db)):
    order = db.get(Order, oid)
    if not order: raise HTTPException(status_code=404, detail="order not found")
    product = db.get(Product, data.product_id)
    if not product: raise HTTPException(status_code=404, detail="product not found")
    
    # Reserve stock using inventory service
    try:
        reserve_stock(db, data.product_id, data.qty, "order_item_create")
    except HTTPException as e:
        raise e  # Re-raise the HTTP exception from inventory service
    
    it = OrderItem(order_id=oid, product_id=data.product_id, qty=data.qty,
                   unit_price=data.unit_price, subtotal=round(data.qty * data.unit_price, 2))
    db.add(it); db.commit(); db.refresh(it)
    _recalc_total(db, oid)
    return it

@router.put("/{oid}/items/{iid}", response_model=OrderItemOut, dependencies=[Depends(require_role("admin"))])
def update_item(oid: int, iid: int, data: OrderItemUpdate, db: Session = Depends(get_db)):
    it = db.get(OrderItem, iid)
    if not it or it.order_id != oid: raise HTTPException(status_code=404, detail="item not found")
    
    # Adjust stock reservations if quantity changes
    if data.qty is not None and data.qty != it.qty:
        diff = data.qty - it.qty
        if diff > 0:
            # Need to reserve more stock
            try:
                reserve_stock(db, it.product_id, diff, "order_item_update")
            except HTTPException as e:
                raise e
        else:
            # Need to release some stock
            release_stock(db, it.product_id, -diff, "order_item_update")
        it.qty = data.qty
    
    if data.unit_price is not None:
        it.unit_price = data.unit_price
    it.subtotal = round(it.qty * float(it.unit_price), 2)
    db.commit(); db.refresh(it)
    _recalc_total(db, oid)
    return it

@router.delete("/{oid}/items/{iid}", dependencies=[Depends(require_role("admin"))])
def delete_item(oid: int, iid: int, db: Session = Depends(get_db)):
    it = db.get(OrderItem, iid)
    if not it or it.order_id != oid: raise HTTPException(status_code=404, detail="item not found")
    
    # Release reserved stock
    release_stock(db, it.product_id, it.qty, "order_item_delete")
    
    db.delete(it); db.commit()
    _recalc_total(db, oid)
    return {"ok": True}
