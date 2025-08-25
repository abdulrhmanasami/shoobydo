#!/usr/bin/env python3
"""
Script: create_tables_simple
Created by: Cursor (auto-generated)
Purpose: إنشاء الجداول واحداً تلو الآخر لتجنب التضارب
Last updated: 2025-08-24
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# إضافة المجلد الحالي إلى Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import Base, engine

def create_tables_one_by_one():
    """إنشاء الجداول واحداً تلو الآخر"""
    try:
        print("🔄 إنشاء الجداول واحداً تلو الآخر...")
        
        # إنشاء جدول suppliers أولاً
        print("📋 إنشاء جدول suppliers...")
        from app.models import Supplier
        Supplier.__table__.create(engine, checkfirst=True)
        
        # إنشاء جدول users
        print("📋 إنشاء جدول users...")
        from app.models_user import User
        User.__table__.create(engine, checkfirst=True)
        
        # إنشاء جدول products
        print("📋 إنشاء جدول products...")
        from app.models_product import Product
        Product.__table__.create(engine, checkfirst=True)
        
        # إنشاء جدول customers
        print("📋 إنشاء جدول customers...")
        from app.models_customer import Customer
        Customer.__table__.create(engine, checkfirst=True)
        
        # إنشاء جدول orders
        print("📋 إنشاء جدول orders...")
        from app.models_order import Order
        Order.__table__.create(engine, checkfirst=True)
        
        # إنشاء جدول order_items
        print("📋 إنشاء جدول order_items...")
        from app.models_order_item import OrderItem
        OrderItem.__table__.create(engine, checkfirst=True)
        
        # إنشاء جدول stock_movements
        print("📋 إنشاء جدول stock_movements...")
        from app.models_stock_movement import StockMovement
        StockMovement.__table__.create(engine, checkfirst=True)
        
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
    create_tables_one_by_one()
