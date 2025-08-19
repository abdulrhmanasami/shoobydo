from __future__ import annotations

"""
Router: auth
Created by: Cursor (auto-generated)
Purpose: Login/refresh/logout endpoints returning JWTs
Last updated: 2025-08-19
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models_user import User
from app.schemas_auth import Token, UserLogin, UserRegister, UserPublic
from app.security import create_access_token, verify_password, get_password_hash
from app.dependencies.auth import require_user


router = APIRouter()
_bearer = HTTPBearer(auto_error=False)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Ensure role claim uses enum value
    role_value = user.role.value if hasattr(user.role, "value") else str(user.role)
    token = create_access_token(str(user.id), role=role_value)
    return Token(access_token=token)


@router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # password policy: min 8, upper, lower, digit
    pw = payload.password or ""
    if not (len(pw) >= 8 and any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Weak password")
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    from app.models_user import UserRole
    role_in = (payload.role or "viewer").lower()
    role_value = role_in if role_in in {"admin","manager","viewer"} else "viewer"
    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role=UserRole(role_value),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserPublic(
        id=str(user.id), email=user.email, role=getattr(user.role, "value", str(user.role)), is_active=user.is_active, created_at=str(user.created_at)
    )


@router.post("/refresh", response_model=Token)
def refresh(current_user = Depends(require_user)):
    # Mint a new token using the currently authenticated user
    role_value = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    new_token = create_access_token(str(current_user.id), role=role_value)
    return Token(access_token=new_token)


@router.post("/logout")
def logout():
    # Stateless JWT logout stub (client should discard token)
    return {"ok": True}


