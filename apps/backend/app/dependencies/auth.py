from __future__ import annotations

"""
Module: dependencies.auth
Created by: Cursor (auto-generated)
Purpose: FastAPI dependencies for authentication and role-based access control
Last updated: 2025-08-20
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.app.db import get_db
from apps.backend.app.models_user import User
from app.security import decode_token


bearer_scheme = HTTPBearer(auto_error=False)


def require_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or missing user")
    return user


def require_role(required: str):
    def _role_guard(user = Depends(require_user)):
        role_value = getattr(user, "role", None)
        try:
            from enum import Enum as _PyEnum
            if isinstance(role_value, _PyEnum):
                role_str = str(role_value.value).lower()
            else:
                role_str = str(role_value).lower() if role_value is not None else ""
        except Exception:
            role_str = str(role_value).lower() if role_value is not None else ""
        if role_str != required:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return _role_guard


def require_any_role(*roles: str):
    allowed = {r.lower() for r in roles}
    def _guard(user = Depends(require_user)):
        role_value = getattr(user, "role", None)
        role_str = getattr(role_value, "value", role_value)
        role_str = str(role_str).lower() if role_str is not None else ""
        if role_str not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return _guard


