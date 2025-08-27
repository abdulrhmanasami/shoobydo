from __future__ import annotations

"""
Router: admin
Created by: Cursor (auto-generated)
Purpose: Admin-only endpoints protected by role guard
Last updated: 2025-08-20
"""

from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role


router = APIRouter()


@router.get("/ping")
def admin_ping(user = Depends(require_role("admin"))):
    return {"ok": True, "user": str(getattr(user, "email", "admin"))}


