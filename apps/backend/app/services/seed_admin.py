from __future__ import annotations

"""
Seed script: creates an admin user if missing; logs outcome.
"""

import os
import uuid

from sqlalchemy.orm import Session

from apps.backend.app.db import SessionLocal
from apps.backend.app.models_user import User, UserRole
from app.security import get_password_hash


def seed_admin() -> None:
    db: Session = SessionLocal()
    try:
        email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("ADMIN_PASSWORD", "admin123")
        existing = db.query(User).filter(User.email == email).one_or_none()
        if existing:
            print(f"[seed] admin already exists: {existing.email} (role={existing.role})")
            return
        admin = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"[seed] admin: {admin.email} (role={admin.role})")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()


