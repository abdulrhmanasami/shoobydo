from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db import get_db
from app.dependencies.auth import require_user, require_any_role
from app.models_customer import Customer
from app.schemas_customer import CustomerCreate, CustomerUpdate, CustomerOut

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=list[CustomerOut])
def list_customers(q: str | None = Query(default=None), db: Session = Depends(get_db), user=Depends(require_user)):
    qs = db.query(Customer)
    if q:
        like = f"%{q}%"
        qs = qs.filter(or_(Customer.email.ilike(like), Customer.name.ilike(like)))
    return qs.order_by(Customer.id.desc()).limit(200).all()

@router.post("/", response_model=CustomerOut, dependencies=[Depends(require_any_role("admin","manager"))])
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    if db.query(Customer).filter(Customer.email==data.email).first():
        raise HTTPException(status_code=409, detail="email exists")
    obj = Customer(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

@router.put("/{cid}", response_model=CustomerOut, dependencies=[Depends(require_any_role("admin","manager"))])
def update_customer(cid: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    obj = db.get(Customer, cid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    patch = data.model_dump(exclude_none=True)
    if "email" in patch:
        exists = db.query(Customer).filter(Customer.email==patch["email"], Customer.id!=cid).first()
        if exists: raise HTTPException(status_code=409, detail="email exists")
    for k, v in patch.items(): setattr(obj, k, v)
    db.commit(); db.refresh(obj); return obj

@router.delete("/{cid}", dependencies=[Depends(require_any_role("admin"))])
def delete_customer(cid: int, db: Session = Depends(get_db)):
    obj = db.get(Customer, cid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    db.delete(obj); db.commit(); return {"ok": True}
