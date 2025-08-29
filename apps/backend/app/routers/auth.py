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
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.models_user import User, UserRole
from app.schemas_auth import UserCreate, UserLogin, Token, UserOut, TokenPair
from app.security import hash_password, verify_password, create_access_token, get_current_user, create_refresh_token, verify_refresh_token

router = APIRouter()
_bearer = HTTPBearer(auto_error=False)

# في الذاكرة (يمكن نقلها لـ Redis لاحقاً)
blacklisted_tokens = set()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    تسجيل مستخدم جديد
    - يسمح فقط بإنشاء أول مستخدم بدون مصادقة (bootstrap)
    - المستخدمين اللاحقين يتطلبون صلاحيات admin
    """
    # bootstrap: أول مستخدم فقط
    users_count = db.query(User).count()
    if users_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Registration is disabled - only first user allowed"
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
        # أول مستخدم = admin
        user = User(
            email=payload.email.lower(),
            password_hash=hash_password(payload.password),
            role=UserRole.admin,  # إجبارياً admin
            is_active=True
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
    access_token = create_access_token({"sub": str(user.id), "type": "access"})
    refresh_token = create_access_token({"sub": str(user.id), "type": "refresh"}, expires_minutes=60*24*14)
    
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
        user_id = payload.get("sub")
        
        user = db.get(User, int(str(user_id))) or db.query(User).filter(User.id == int(str(user_id))).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # إنشاء access token جديد
        new_access_token = create_access_token({"sub": str(user.id), "type": "access"})
        
        return Token(
            access_token=new_access_token,
            token_type="bearer"
        )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
def logout(
    user: User = Depends(get_current_user),
    token: HTTPAuthorizationCredentials = Depends(_bearer)
):
    """
    تسجيل الخروج وإضافة التوكن للقائمة السوداء
    """
    if token and token.credentials:
        try:
            from jose import jwt
            from app.security import SECRET_KEY, JWT_ALGORITHM
            from datetime import datetime, timezone
            
            # فك التوكن لاستخراج jti و exp
            payload = jwt.decode(
                token.credentials, 
                SECRET_KEY, 
                algorithms=[JWT_ALGORITHM], 
                options={"verify_aud": False}
            )
            
            jti = payload.get("jti", "")
            exp = payload.get("exp", 0)
            
            if jti and exp:
                # حساب TTL المتبقي
                now = int(datetime.now(timezone.utc).timestamp())
                ttl = max(0, int(exp) - now)
                
                # إضافة للقائمة السوداء
                try:
                    from app.security_blacklist import blacklist
                    blacklist(jti, ttl)
                except ImportError:
                    # Redis غير متوفر في البيئة المحلية
                    pass
        except Exception:
            # في حالة فشل فك التوكن، تجاهل
            pass
    
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    """
    الحصول على معلومات المستخدم الحالي
    """
    return UserOut(id=user.id, email=user.email, role=user.role.value, is_active=user.is_active)

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


