from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.db import get_db
from app.dependencies.auth import require_user, require_any_role
from app.models_order import Order
from app.models_product import Product
from app.models_order_item import OrderItem
from app.services.orders_total import recalc_order_total
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
def list_items(oid: int = Path(..., ge=1), db: Session = Depends(get_db), user=Depends(require_user)):
    if not db.get(Order, oid):
        raise HTTPException(status_code=404, detail="order not found")
    return db.query(OrderItem).filter_by(order_id=oid).order_by(OrderItem.id.desc()).all()

@router.post("/{oid}/items", response_model=OrderItemOut, dependencies=[Depends(require_any_role("admin","manager"))])
def add_item(oid: int, data: OrderItemCreate, db: Session = Depends(get_db)):
    order = db.get(Order, oid)
    if not order: raise HTTPException(status_code=404, detail="order not found")
    product = db.get(Product, data.product_id)
    if not product: raise HTTPException(status_code=404, detail="product not found")
    if product.stock is None or product.stock < data.qty:
        raise HTTPException(status_code=409, detail="insufficient stock")
    product.stock -= data.qty
    it = OrderItem(order_id=oid, product_id=data.product_id, qty=data.qty,
                   unit_price=data.unit_price, subtotal=round(data.qty * data.unit_price, 2))
    db.add(it); db.commit(); db.refresh(it)
    _recalc_total(db, oid)
    return it

@router.put("/{oid}/items/{iid}", response_model=OrderItemOut, dependencies=[Depends(require_any_role("admin","manager"))])
def update_item(oid: int, iid: int, data: OrderItemUpdate, db: Session = Depends(get_db)):
    it = db.get(OrderItem, iid)
    if not it or it.order_id != oid: raise HTTPException(status_code=404, detail="item not found")
    # adjust stock if qty changes
    if data.qty is not None and data.qty != it.qty:
        diff = data.qty - it.qty
        prod = db.get(Product, it.product_id)
        if diff > 0:
            if prod.stock < diff: raise HTTPException(status_code=409, detail="insufficient stock")
            prod.stock -= diff
        else:
            prod.stock += (-diff)
        it.qty = data.qty
    if data.unit_price is not None:
        it.unit_price = data.unit_price
    it.subtotal = round(it.qty * float(it.unit_price), 2)
    db.commit(); db.refresh(it)
    _recalc_total(db, oid)
    return it

@router.delete("/{oid}/items/{iid}", dependencies=[Depends(require_any_role("admin"))])
def delete_item(oid: int, iid: int, db: Session = Depends(get_db)):
    it = db.get(OrderItem, iid)
    if not it or it.order_id != oid: raise HTTPException(status_code=404, detail="item not found")
    prod = db.get(Product, it.product_id)
    prod.stock += it.qty
    db.delete(it); db.commit()
    _recalc_total(db, oid)
    return {"ok": True}
