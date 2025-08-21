from __future__ import annotations

"""
Module: security
Created by: Cursor (auto-generated)
Purpose: Password hashing utilities and JWT token helpers
Last updated: 2025-08-20
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _jwt_settings() -> tuple[str, str, int]:
    secret_key = os.getenv("JWT_SECRET_KEY", "changeme-in-dev")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    expires_minutes = int(os.getenv("JWT_EXPIRES_MINUTES", "30"))
    return secret_key, algorithm, expires_minutes


def create_access_token(subject: str, role: str, expires_minutes: int | None = None) -> str:
    secret_key, algorithm, default_exp = _jwt_settings()
    exp_minutes = expires_minutes if expires_minutes is not None else default_exp
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=exp_minutes)
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(token: str) -> Dict[str, Any]:
    secret_key, algorithm, _ = _jwt_settings()
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


