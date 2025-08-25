"""
Router: reports
Created by: Cursor (auto-generated)
Purpose: Reports and KPIs with Redis caching
Last updated: 2025-08-24
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
from app.db import get_db
from app.security import require_role
from app.services.redis_store import get_redis
from app.models import Supplier
from app.models_product import Product
from app.models_order import Order
from app.models_customer import Customer
import json

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/kpis", dependencies=[Depends(require_role("admin", "viewer"))])
def get_kpis(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get KPIs with Redis caching"""
    redis = get_redis()
    cache_key = "kpis:v1:summary"
    
    # Try cache first
    if redis:
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)
    
    # Calculate KPIs
    total_suppliers = db.query(Supplier).count()
    total_products = db.query(Product).count()
    total_customers = db.query(Customer).count()
    total_orders = db.query(Order).count()
    
    # Calculate total rows from suppliers
    total_rows = db.query(func.coalesce(func.sum(Supplier.rows), 0)).scalar() or 0
    total_sheets = db.query(func.coalesce(func.sum(Supplier.sheets), 0)).scalar() or 0
    
    # Calculate revenue
    total_revenue = db.query(func.coalesce(func.sum(Order.total), 0)).scalar() or 0
    
    kpis = {
        "suppliers": total_suppliers,
        "products": total_products,
        "customers": total_customers,
        "orders": total_orders,
        "files": total_suppliers,  # Each supplier = 1 file
        "rows": total_rows,
        "sheets": total_sheets,
        "revenue": float(total_revenue),
        "notes": "Calculated from database"
    }
    
    # Cache for 5 minutes
    if redis:
        redis.setex(cache_key, 300, json.dumps(kpis))
    
    return kpis


@router.get("/summary", dependencies=[Depends(require_role("admin", "viewer"))])
def get_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get summary statistics with Redis caching"""
    redis = get_redis()
    cache_key = "summary:v1:overview"
    
    # Try cache first
    if redis:
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)
    
    # Calculate summary
    summary = {
        "suppliers": db.query(Supplier).count(),
        "kpis": {
            "files": db.query(Supplier).count(),
            "rows": db.query(func.coalesce(func.sum(Supplier.rows), 0)).scalar() or 0,
            "sheets": db.query(func.coalesce(func.sum(Supplier.sheets), 0)).scalar() or 0
        },
        "notes": "Database summary"
    }
    
    # Cache for 5 minutes
    if redis:
        redis.setex(cache_key, 300, json.dumps(summary))
    
    return summary


@router.get("/costs", dependencies=[Depends(require_role("admin", "viewer"))])
def get_costs(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get cost analysis with Redis caching"""
    redis = get_redis()
    cache_key = "costs:v1:analysis"
    
    # Try cache first
    if redis:
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)
    
    # Calculate costs (placeholder - replace with actual cost logic)
    total_suppliers = db.query(Supplier).count()
    total_rows = db.query(func.coalesce(func.sum(Supplier.rows), 0)).scalar() or 0
    
    # Estimate costs based on data volume (example calculation)
    estimated_cost_per_row = 0.01  # €0.01 per row
    total_cost = total_rows * estimated_cost_per_row
    total_margin = total_cost * 0.3  # 30% margin
    
    costs = {
        "files": total_suppliers,
        "rows": total_rows,
        "total_cost": round(total_cost, 2),
        "total_margin": round(total_margin, 2),
        "notes": "Estimated costs based on data volume"
    }
    
    # Cache for 10 minutes
    if redis:
        redis.setex(cache_key, 600, json.dumps(costs))
    
    return costs


@router.post("/refresh", dependencies=[Depends(require_role("admin"))])
def refresh_reports(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Force refresh all cached reports"""
    redis = get_redis()
    if redis:
        # Clear all report caches
        keys = redis.keys("kpis:v1:*") + redis.keys("summary:v1:*") + redis.keys("costs:v1:*")
        if keys:
            redis.delete(*keys)
    
    return {"message": "Reports cache cleared", "refreshed": True}
