"""
Inventory Management Router

Provides endpoints for stock management, reservations, and adjustments.
Admin and manager access required for most operations.

Author: Cursor (auto-generated)
Purpose: Inventory management API endpoints
Last updated: 2025-08-21
"""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.db import get_db
from app.security import require_role
from app.services.inventory import (
    reserve_stock, release_stock, adjust_stock_on_hand, get_stock_status
)
from pydantic import BaseModel
from typing import Optional


router = APIRouter(prefix="/inventory", tags=["inventory"])


class StockAdjustmentRequest(BaseModel):
    adjustment: int
    reason: str = "manual_adjust"
    notes: Optional[str] = None


@router.get("/products/{product_id}/stock")
def get_product_stock(
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Get current stock status for a product."""
    status = get_stock_status(db, product_id)
    if not status:
        raise HTTPException(status_code=404, detail="Product not found")
    return status


@router.post("/products/{product_id}/adjust", dependencies=[Depends(require_any_role("admin", "manager"))])
def adjust_product_stock(
    request: StockAdjustmentRequest,
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Manually adjust stock on hand (admin/manager only)."""
    success = adjust_stock_on_hand(
        db, product_id, request.adjustment, request.reason, request.notes
    )
    if success:
        return {"message": "Stock adjusted successfully", "product_id": product_id}
    raise HTTPException(status_code=400, detail="Invalid adjustment")


@router.post("/products/{product_id}/reserve")
def reserve_product_stock(
    quantity: int = Path(..., ge=1),
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Reserve stock for a product."""
    success = reserve_stock(db, product_id, quantity, "reserve")
    if success:
        return {"message": "Stock reserved successfully", "product_id": product_id, "quantity": quantity}
    raise HTTPException(status_code=400, detail="Reservation failed")


@router.post("/products/{product_id}/release")
def release_product_stock(
    quantity: int = Path(..., ge=1),
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    """Release previously reserved stock."""
    success = release_stock(db, product_id, quantity, "release")
    if success:
        return {"message": "Stock released successfully", "product_id": product_id, "quantity": quantity}
    raise HTTPException(status_code=400, detail="Release failed")
