from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models_user import User
from ..security import get_current_user

router = APIRouter(prefix="/_diag", tags=["_diag"], include_in_schema=False)

@router.get("/db")
def diag_db(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {
        "engine": str(db.get_bind().url).split("///")[-1],
        "users_count": len(users),
        "all_users": [{"id": u.id, "email": u.email, "active": getattr(u,"is_active",True)} for u in users],
    }

@router.get("/me")
def diag_me(user: User = Depends(get_current_user)):
    return {"user_id": user.id, "email": user.email, "active": user.is_active}
