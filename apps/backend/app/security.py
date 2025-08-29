# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import uuid

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
    payload["jti"] = payload.get("jti", uuid.uuid4().hex)  # JWT ID للقائمة السوداء
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
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_aud": False})
        
        # فحص نوع التوكن
        tt = payload.get("type")
        if tt != "access":
            raise HTTPException(
                status_code=401, 
                detail="Invalid token type", 
                headers={"WWW-Authenticate":"Bearer"}
            )
        
        # فحص القائمة السوداء
        try:
            from .security_blacklist import is_blacklisted
            jti = payload.get("jti", "")
            if is_blacklisted(jti):
                raise HTTPException(
                    status_code=401, 
                    detail="Token revoked", 
                    headers={"WWW-Authenticate":"Bearer"}
                )
        except ImportError:
            # Redis غير متوفر في البيئة المحلية
            pass
        
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


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def require_role(*roles: str):
    """Dependency to require specific user roles."""
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker

def create_refresh_token(data: Dict, expires_minutes: Optional[int] = None) -> str:
    """Create a refresh token."""
    now = datetime.now(timezone.utc)
    exp_min = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES * 2  # Refresh tokens last longer
    payload = dict(data or {})
    if "sub" in payload and payload["sub"] is not None:
        payload["sub"] = str(payload["sub"])
    payload.setdefault("type", "refresh")
    payload["jti"] = payload.get("jti", uuid.uuid4().hex)  # JWT ID للقائمة السوداء
    payload["iat"] = int(now.timestamp())
    payload["nbf"] = int(now.timestamp())
    payload["exp"] = int((now + timedelta(minutes=exp_min)).timestamp())
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_refresh_token(token: str) -> Dict:
    """Verify and decode a refresh token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_aud": False})
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
