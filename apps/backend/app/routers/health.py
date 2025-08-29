from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter()

@router.get("/health")
def health(db: Session = Depends(get_db)):
    """
    Health check موسّع مع فحص قاعدة البيانات
    """
    try:
        # فحص قاعدة البيانات
        db.execute("SELECT 1")
        db_status = True
    except Exception:
        db_status = False
    
    if db_status:
        return {"status": "ok", "db": True, "timestamp": "2025-01-28T00:00:00Z"}
    else:
        return {"status": "degraded", "db": False, "timestamp": "2025-01-28T00:00:00Z"}
