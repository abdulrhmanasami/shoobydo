#!/usr/bin/env python3
"""
Script: create_tables
Created by: Cursor (auto-generated)
Purpose: إنشاء جميع الجداول في قاعدة البيانات
Last updated: 2025-08-24
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# إضافة المجلد الحالي إلى Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import Base, engine
from app.models import Supplier
from app.models_user import User, UserRole
from app.models_product import Product
from app.models_customer import Customer
from app.models_order import Order
from app.models_order_item import OrderItem
from app.models_stock_movement import StockMovement

def create_all_tables():
    """إنشاء جميع الجداول"""
    try:
        print("🔄 إنشاء الجداول...")
        
        # إنشاء جميع الجداول
        Base.metadata.create_all(bind=engine)
        
        print("✅ تم إنشاء جميع الجداول بنجاح!")
        
        # التحقق من الجداول
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            print(f"📋 الجداول الموجودة: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_all_tables()
