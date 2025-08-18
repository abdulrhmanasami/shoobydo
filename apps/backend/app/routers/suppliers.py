from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import os

from app.db import get_db
from app.models import Supplier
from app.schemas import SupplierOut, SupplierStats

router = APIRouter()


@router.get("/", response_model=List[SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).order_by(Supplier.id.asc()).all()


@router.get("/stats", response_model=SupplierStats)
def supplier_stats(db: Session = Depends(get_db)):
    total = db.query(Supplier).count()
    agg_rows = 0
    agg_sheets = 0
    if total:
        for s in db.query(Supplier.rows, Supplier.sheets).all():
            agg_rows += int(s.rows or 0)
            agg_sheets += int(s.sheets or 0)
    return SupplierStats(total=total, files=total, rows=agg_rows, sheets=agg_sheets, notes="ok")


@router.post("/reindex")
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


