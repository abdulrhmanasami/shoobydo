from __future__ import annotations

"""
Module: schemas_auth
Created by: Cursor (auto-generated)
Purpose: Pydantic schemas for Auth flows (login, token, user output)
Last updated: 2025-08-20
"""

from typing import Literal
from pydantic import ConfigDict
from pydantic import BaseModel

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    role: Literal["admin","manager","viewer"]
    is_active: bool

class UserCreate(BaseModel):
    email: str
    password: str
    role: Literal["admin","manager","viewer"] = "viewer"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    email: str
    password: str
    confirm_password: str

class UserPublic(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
