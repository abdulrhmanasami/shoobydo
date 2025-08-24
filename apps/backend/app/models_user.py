from __future__ import annotations
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum, DateTime, func
from app.db import Base

class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.viewer)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    viewer = "viewer"
