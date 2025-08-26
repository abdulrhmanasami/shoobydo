from __future__ import annotations

"""
Module: security
Created by: Cursor (auto-generated)
Purpose: Password hashing utilities and JWT token helpers
Last updated: 2025-08-24
"""

import os
import datetime as dt
import time
from typing import Annotated, Callable, Literal
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db import get_db  # افترض موجود
from app.models_user import User, UserRole

# إعدادات
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "30"))
REFRESH_TOKEN_EXPIRES_MINUTES = int(os.getenv("JWT_REFRESH_EXPIRES_MINUTES", "10080"))
JWT_SKEW_SECONDS = int(os.getenv('JWT_SKEW_SECONDS','300'))  # 5min

# استخدام HTTPBearer بدلاً من OAuth2PasswordBearer لتجنب مشاكل tokenUrl
oauth2_scheme = HTTPBearer(auto_error=False)
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return pwd.verify(p, hashed)

def create_access_token(sub: str, role: str) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    exp = now + dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "role": role, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(sub: str) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    exp = now + dt.timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
    payload = {"sub": sub, "type": "refresh", "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

def get_bearer_token(authorization: str | None = Header(default=None)) -> str:
    """جامع التوكن من الهيدر مباشرة"""
    if authorization and authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    raise HTTPException(status_code=401, detail="Invalid credentials")

def jwt_decode_secure(token: str) -> dict:
    """فك JWT بتوقيع مُتحقق + exp يدوي بسماحية"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False, "verify_aud": False})
    exp = payload.get("exp")
    if exp is not None:
        now = int(time.time())
        if now > int(exp) + JWT_SKEW_SECONDS:
            raise HTTPException(status_code=401, detail="Token expired")
    return payload

def get_current_user(
    token: str = Depends(get_bearer_token),
    db: Session = Depends(get_db)
) -> User:
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    
    if not token:
        raise cred_exc
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise cred_exc
    return user

def require_role(*roles: Literal["admin","manager","viewer"]) -> Callable:
    def dep(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dep
