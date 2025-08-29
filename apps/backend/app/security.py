# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from sqlalchemy.orm import Session

# --- إعدادات مرنة: من config إن وُجد، وإلا من البيئة مع افتراضات آمنة ---
try:
    # إن كان لديك settings (غير موجود لدى بعض الفروع)
    from .config import settings  # type: ignore
    SECRET_KEY = getattr(settings, "SECRET_KEY")
    JWT_ALGORITHM = getattr(settings, "JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 120))
    LEEWAY_SECONDS = int(getattr(settings, "JWT_LEEWAY_SECONDS", 10))
except Exception:
    import os
    SECRET_KEY = os.getenv("SECRET_KEY", "shoobydo-dev-secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    LEEWAY_SECONDS = int(os.getenv("JWT_LEEWAY_SECONDS", "10"))

# DB deps (مهم جدًا توحيد المسار)
from .db import get_db
from .models_user import User

oauth2_scheme = HTTPBearer(auto_error=True)  # 401 نظيفة عند غياب التوكن


def create_access_token(data: Dict, expires_minutes: Optional[int] = None) -> str:
    """
    ينشئ JWT مع iat/nbf/exp. يحوّل sub إلى نص لضمان التوافق مع jose.
    """
    now = datetime.now(timezone.utc)
    exp_min = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    payload = dict(data or {})
    # sub نصي دائمًا
    if "sub" in payload and payload["sub"] is not None:
        payload["sub"] = str(payload["sub"])
    payload.setdefault("type", "access")
    payload["iat"] = int(now.timestamp())
    payload["nbf"] = int(now.timestamp())
    payload["exp"] = int((now + timedelta(minutes=exp_min)).timestamp())
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    يستخرج Bearer token بشكل صحيح، يفكّه، ويجلب المستخدم بالـ id من sub.
    """
    if not token or not getattr(token, "credentials", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_aud": False},
            leeway=LEEWAY_SECONDS,
        )
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user_id = int(sub)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: non-integer sub",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, user_id) or db.query(User).filter(User.id == user_id).first()
    if not user or not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or missing user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
