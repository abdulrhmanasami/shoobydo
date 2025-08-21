from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db import get_db
from app.dependencies.auth import require_user, require_any_role
from app.models_order import Order
from app.models_customer import Customer
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
