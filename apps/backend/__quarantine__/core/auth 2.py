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
from app.models_user import User
from app.schemas_auth import Token, UserLogin, UserRegister, UserPublic, TokenPair
from app.security import create_access_token, verify_password, get_password_hash
from app.dependencies.auth import require_user
from app.services.tokens import (
    create_access_token as create_access_token_pair,
    create_refresh_token,
    rotate_refresh,
    decode_refresh,
    blacklist_refresh_jti,
)


router = APIRouter()
_bearer = HTTPBearer(auto_error=False)


@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Ensure role claim uses enum value
    role_value = user.role.value if hasattr(user.role, "value") else str(user.role)
    access, _ = create_access_token_pair(str(user.id), role=role_value)
    refresh, _, _ = create_refresh_token(str(user.id), role=role_value)
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    # password policy: min 8, upper, lower, digit
    pw = (payload.password or "").strip()
    if not (len(pw) >= 8 and any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Weak password")
    # basic email validation + normalization
    email_normalized = (payload.email or "").strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_normalized):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email")
    exists = db.query(User).filter(User.email == email_normalized).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    from app.models_user import UserRole
    role_in = (payload.role or "viewer").lower()
    role_value = role_in if role_in in {"admin","manager","viewer"} else "viewer"
    user = User(
        email=email_normalized,
        hashed_password=get_password_hash(payload.password),
        role=UserRole(role_value),
        is_active=True,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    db.refresh(user)
    return UserPublic(
        id=str(user.id), email=user.email, role=getattr(user.role, "value", str(user.role)), is_active=user.is_active, created_at=str(user.created_at)
    )


from fastapi import Header


@router.post("/refresh", response_model=TokenPair)
def refresh(authorization: str | None = Header(None)):
    # Expect refresh token in Authorization header; rotate and blacklist old
    token = authorization
    if not token:
        raise HTTPException(status_code=401, detail="missing Authorization")
    parts = token.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="invalid Authorization")
    rt = parts[1]
    try:
        new_refresh, _, _ = rotate_refresh(rt)
        claims = decode_refresh(new_refresh)
        new_access, _ = create_access_token_pair(str(claims["sub"]), role=claims.get("role", "viewer"))
        return TokenPair(access_token=new_access, refresh_token=new_refresh)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
def logout(authorization: str = Depends(lambda authorization: authorization)):
    if not authorization:
        return {"ok": True}
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        try:
            claims = decode_refresh(parts[1])
            jti = claims.get("jti")
            if jti:
                blacklist_refresh_jti(jti, claims.get("exp"))
        except Exception:
            pass
    return {"ok": True}


