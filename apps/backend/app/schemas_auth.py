from __future__ import annotations

"""
Module: schemas_auth
Created by: Cursor (auto-generated)
Purpose: Pydantic schemas for Auth flows (login, token, user output)
Last updated: 2025-08-20
"""

from typing import Literal

from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


