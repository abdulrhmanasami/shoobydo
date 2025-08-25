from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os

from app.db import get_db
from app.models import Supplier
from app.schemas import SupplierOut, SupplierStats, SupplierIn, SupplierUpdate
from app.security import get_current_user, require_role

router = APIRouter(prefix="", tags=["suppliers"], redirect_slashes=False)


@router.get("/", response_model=List[SupplierOut], dependencies=[Depends(get_current_user)])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).order_by(Supplier.id.asc()).all()


@router.get("", include_in_schema=False)
def list_suppliers_noslash(db: Session = Depends(get_db)):
    return list_suppliers(db)


@router.get("/stats", response_model=SupplierStats, dependencies=[Depends(get_current_user)])
def supplier_stats(db: Session = Depends(get_db)):
    total = db.query(Supplier).count()
    agg_rows = 0
    agg_sheets = 0
    if total:
        for s in db.query(Supplier.rows, Supplier.sheets).all():
            agg_rows += int(s.rows or 0)
            agg_sheets += int(s.sheets or 0)
    return SupplierStats(total=total, files=total, rows=agg_rows, sheets=agg_sheets, notes="ok")


@router.post("/upload")
async def upload_supplier_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in {"text/csv","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","application/vnd.ms-excel"}:
        raise HTTPException(status_code=415, detail="Unsupported file type")
    data_dir = os.getenv("DATA_DIR", "data/uploads")
    os.makedirs(data_dir, exist_ok=True)
    dest = os.path.join(data_dir, file.filename)
    # حد الحجم ~10MB
    CHUNK = 1<<20
    size = 0
    with open(dest, "wb") as f:
        while True:
            chunk = await file.read(CHUNK)
            if not chunk: break
            size += len(chunk)
            if size > 10*(1<<20):
                f.close(); os.remove(dest)
                raise HTTPException(status_code=413, detail="File too large")
            f.write(chunk)

    # فهرسة خفيفة (حساب عدد الصفوف/الأوراق إن XLSX)
    rows = 0; sheets = 0
    try:
        if dest.lower().endswith(".csv"):
            with open(dest, "rb") as fh:
                rows = sum(1 for _ in fh) - 1
            sheets = 1
        else:
            import pandas as pd
            import openpyxl  # تأكد أنها بالـ requirements
            xl = pd.ExcelFile(dest)
            sheets = len(xl.sheet_names)
            for nm in xl.sheet_names:
                try: rows += int(xl.parse(nm).shape[0])
                except Exception: pass
    except Exception as e:
        # لا نُفشل الرفع بسبب pandas/openpyxl
        pass

    from app.models import Supplier
    name = os.path.splitext(os.path.basename(dest))[0]
    obj = db.query(Supplier).filter(Supplier.file_path==dest).one_or_none()
    if obj:
        obj.name, obj.rows, obj.sheets = name, rows, sheets
    else:
        obj = Supplier(name=name, file_path=dest, rows=rows, sheets=sheets)
        db.add(obj)
    db.commit(); db.refresh(obj)
    return {"id": obj.id, "name": obj.name, "rows": obj.rows, "sheets": obj.sheets, "file_path": obj.file_path}


@router.post("/reindex", dependencies=[Depends(require_role("admin"))])
def reindex_suppliers(db: Session = Depends(get_db)):
    # Scan data directory recursively for .xlsx files
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data"))
    found_files = []
    if os.path.isdir(data_dir):
        for root, _, files in os.walk(data_dir):
            for f in files:
                if f.lower().endswith(".xlsx"):
                    found_files.append(os.path.join(root, f))

    import pandas as pd
    updated = 0
    for path in found_files:
        try:
            xl = pd.ExcelFile(path)
            sheet_names = list(xl.sheet_names)
            total_rows = 0
            for name in sheet_names:
                try:
                    df = xl.parse(name)
                    total_rows += int(df.shape[0])
                except Exception:
                    pass
            name = os.path.splitext(os.path.basename(path))[0]
            existing = db.query(Supplier).filter(Supplier.file_path == path).one_or_none()
            if existing:
                existing.name = name
                existing.rows = total_rows
                existing.sheets = len(sheet_names)
            else:
                db.add(Supplier(name=name, file_path=path, rows=total_rows, sheets=len(sheet_names)))
            updated += 1
        except Exception:
            # Skip unreadable files
            pass
    db.commit()
    return {"indexed": updated, "files": len(found_files)}


@router.post("/", response_model=SupplierOut, dependencies=[Depends(require_role("admin"))])
def create_supplier(payload: SupplierIn, db: Session = Depends(get_db)):
    entity = Supplier(name=payload.name, file_path=payload.file_path, rows=payload.rows, sheets=payload.sheets)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


@router.delete("/{supplier_id}", dependencies=[Depends(require_role("admin"))])
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), user = Depends(require_role("admin"))):
    obj = db.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(obj)
    db.commit()
    return {"deleted": supplier_id}

@router.get("/{supplier_id}", response_model=SupplierOut, dependencies=[Depends(get_current_user)])
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    obj = db.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return obj

@router.put("/{supplier_id}", response_model=SupplierOut, dependencies=[Depends(require_role("admin"))])
def update_supplier(supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db), user = Depends(require_role("admin"))):
    obj = db.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Supplier not found")
    # ... existing code ...
