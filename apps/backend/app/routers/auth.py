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
from app.schemas_auth import Token, UserLogin
from app.security import create_access_token, verify_password


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


@router.post("/refresh", response_model=Token)
def refresh(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer)):
    # Accept bearer token and re-issue a fresh one (basic demo; production should use refresh tokens)
    from app.security import decode_token
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    new_token = create_access_token(payload.get("sub"), role=payload.get("role", "viewer"))
    return Token(access_token=new_token)


@router.post("/logout")
def logout():
    # Stateless JWT logout stub (client should discard token)
    return {"ok": True}


