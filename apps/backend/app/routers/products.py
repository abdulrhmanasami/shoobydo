from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from apps.backend.app.security import get_current_user, require_role
from apps.backend.app.db import get_db
from app.models_product import Product
from app.schemas_product import ProductCreate, ProductUpdate, ProductOut
router = APIRouter(prefix="/products", tags=["products"])
@router.get("/", response_model=list[ProductOut])
def list_products(q: str | None = None, db: Session = Depends(get_db), user=Depends(require_role)):
    qs = db.query(Product)
    if q: qs = qs.filter(Product.name.ilike(f"%{q}%"))
    return qs.order_by(Product.id.desc()).limit(200).all()
@router.post("/", response_model=ProductOut, dependencies=[Depends(require_role("admin"))])
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    if db.query(Product).filter_by(sku=data.sku).first():
        raise HTTPException(status_code=409, detail="sku exists")
    obj = Product(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj
@router.put("/{pid}", response_model=ProductOut, dependencies=[Depends(require_role("admin"))])
def update_product(pid: int, data: ProductUpdate, db: Session = Depends(get_db)):
    obj = db.get(Product, pid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    for k,v in data.model_dump(exclude_none=True).items(): setattr(obj, k, v)
    db.commit(); db.refresh(obj); return obj
@router.delete("/{pid}", dependencies=[Depends(require_role("admin"))])
def delete_product(pid: int, db: Session = Depends(get_db)):
    obj = db.get(Product, pid)
    if not obj: raise HTTPException(status_code=404, detail="not found")
    db.delete(obj); db.commit(); return {"ok": True}
