from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies.auth import require_user, require_any_role
from app.models_order import Order
from app.schemas_order import OrderCreate, OrderUpdate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[OrderOut])
def list_orders(q: str | None = None, db: Session = Depends(get_db), user=Depends(require_user)):
    qs = db.query(Order)
    if q:
        like = f"%{q}%"
        from sqlalchemy import or_
        qs = qs.filter(or_(Order.customer_email.ilike(like), Order.status.ilike(like)))
    return qs.order_by(Order.id.desc()).limit(200).all()

@router.post("/", response_model=OrderOut, dependencies=[Depends(require_any_role("admin","manager"))])
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    obj = Order(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

@router.put("/{oid}", response_model=OrderOut, dependencies=[Depends(require_any_role("admin","manager"))])
def update_order(oid: int, data: OrderUpdate, db: Session = Depends(get_db)):
    obj = db.get(Order, oid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    for k,v in data.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj); return obj

@router.delete("/{oid}", dependencies=[Depends(require_any_role("admin"))])
def delete_order(oid: int, db: Session = Depends(get_db)):
    obj = db.get(Order, oid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    db.delete(obj); db.commit(); return {"ok": True}
