from __future__ import annotations

"""
Router: auth
Created by: Cursor (auto-generated)
Purpose: Login/refresh/logout endpoints returning JWTs
Last updated: 2025-08-24
"""

from fastapi import APIRouter, Depends, HTTPException, status, Form
import re
from sqlalchemy.exc import IntegrityError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models_user import User, UserRole
from app.schemas_auth import UserCreate, UserLogin, Token, UserOut, TokenPair
from app.security import hash_password, verify_password, create_access_token, get_current_user, require_role, create_refresh_token, verify_refresh_token

router = APIRouter()
_bearer = HTTPBearer(auto_error=False)

# في الذاكرة (يمكن نقلها لـ Redis لاحقاً)
blacklisted_tokens = set()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    تسجيل مستخدم جديد
    - يسمح فقط بإنشاء أول مستخدم بدون مصادقة
    - المستخدمين اللاحقين يتطلبون صلاحيات admin
    """
    # التحقق من وجود مستخدمين
    exists = db.query(User).count()
    if exists > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="التسجيل مغلق - يتطلب صلاحيات مدير"
        )
    
    # التحقق من صحة البريد الإلكتروني
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="صيغة البريد الإلكتروني غير صحيحة"
        )
    
    # التحقق من قوة كلمة المرور
    if len(payload.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور يجب أن تكون 8 أحرف على الأقل"
        )
    
    try:
        user = User(
            email=payload.email.lower(),
            password_hash=hash_password(payload.password),
            role=UserRole(payload.role)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مستخدم بالفعل"
        )

@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    تسجيل الدخول وإرجاع access token و refresh token
    """
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="بيانات الاعتماد غير صحيحة"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="الحساب معطل"
        )
    
    # إنشاء tokens
    access_token = create_access_token(sub=user.email, role=user.role.value)
    refresh_token = create_refresh_token(sub=user.email)
    
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    تجديد access token باستخدام refresh token
    """
    try:
        payload = verify_refresh_token(refresh_token)
        email = payload.get("sub")
        
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # إنشاء access token جديد
        new_access_token = create_access_token(sub=user.email, role=user.role.value)
        
        return Token(
            access_token=new_access_token,
            token_type="bearer"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
def logout(
    user: User = Depends(get_current_user)
):
    """
    تسجيل الخروج وإضافة التوكن للقائمة السوداء
    """
    # في الإنتاج، استخدم Redis للقائمة السوداء
    # blacklisted_tokens.add(token)
    
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
def get_current_user_info(
    user: User = Depends(get_current_user)
):
    """
    الحصول على معلومات المستخدم الحالي
    """
    return user

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    تجديد access token باستخدام refresh token
    """
    try:
        payload = verify_refresh_token(refresh_token)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token غير صالح"
            )
        
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="المستخدم غير موجود أو معطل"
            )
        
        # إنشاء access token جديد
        new_access_token = create_access_token(sub=user.email, role=user.role.value)
        
        return Token(
            access_token=new_access_token,
            token_type="bearer"
        )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token غير صالح"
        )

@router.post("/logout")
def logout(token: str = Depends(_bearer)):
    """
    تسجيل الخروج وإضافة token للقائمة السوداء
    """
    if token:
        blacklisted_tokens.add(token.credentials)
    
    return {"message": "تم تسجيل الخروج بنجاح"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    """
    الحصول على معلومات المستخدم الحالي
    """
    return user

@router.post("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    تغيير كلمة المرور
    """
    # التحقق من كلمة المرور الحالية
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور الحالية غير صحيحة"
        )
    
    # التحقق من قوة كلمة المرور الجديدة
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور الجديدة يجب أن تكون 8 أحرف على الأقل"
        )
    
    # تحديث كلمة المرور
    user.password_hash = hash_password(new_password)
    db.commit()
    
    return {"message": "تم تغيير كلمة المرور بنجاح"}


