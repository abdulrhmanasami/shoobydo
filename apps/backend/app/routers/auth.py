from __future__ import annotations

"""
Router: auth
Created by: Cursor (auto-generated)
Purpose: Login/refresh/logout endpoints returning JWTs
Last updated: 2025-08-19
"""

from fastapi import APIRouter, Depends, HTTPException, status
import re
from sqlalchemy.exc import IntegrityError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models_user import User, UserRole
from app.schemas_auth import UserCreate, UserLogin, Token, UserOut
from app.security import hash_password, verify_password, create_access_token, get_current_user, require_role

router = APIRouter()
_bearer = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # السماح بإنشاء أول مستخدم بدون مصادقة؛ بعده يتطلب admin (خارج نطاق هذا المسار الآن)
    exists = db.query(User).count()
    if exists > 0:
        # بعد أول مستخدم، سجّل مستخدمًا جديدًا عبر admin فقط (تبسيط: رفض)
        raise HTTPException(status_code=403, detail="Registration closed (admin only)")
    user = User(email=payload.email, password_hash=hash_password(payload.password), role=UserRole(payload.role))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user.email, role=user.role.value)
    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


