"""
Inventory Management Service

Handles stock reservations, releases, and movements tracking.
Prevents overselling and maintains accurate stock levels.

Author: Cursor (auto-generated)
Purpose: Inventory management and stock reservations
Last updated: 2025-08-21
"""

from sqlalchemy.orm import Session
from app.models_product import Product
from app.models_stock_movement import StockMovement
from typing import Optional
from fastapi import HTTPException


def reserve_stock(db: Session, product_id: int, quantity: int, reason: str = "reserve") -> bool:
    """
    Reserve stock for a product (e.g., when creating order item).
    
    Args:
        db: Database session
        product_id: ID of the product
        quantity: Quantity to reserve
        reason: Reason for reservation
        
    Returns:
        True if reservation successful, False otherwise
        
    Raises:
        HTTPException: If insufficient stock available
    """
    if quantity <= 0:
        return False
    
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if we have enough stock available
    available_stock = product.stock_on_hand - product.stock_reserved
    if available_stock < quantity:
        raise HTTPException(
            status_code=409, 
            detail=f"Insufficient stock. Available: {available_stock}, Requested: {quantity}"
        )
    
    # Reserve the stock
    product.stock_reserved += quantity
    
    # Record the movement
    movement = StockMovement(
        product_id=product_id,
        qty_change=quantity,
        reason=reason,
        notes=f"Reserved {quantity} units"
    )
    db.add(movement)
    
    db.commit()
    db.refresh(product)
    
    return True


def release_stock(db: Session, product_id: int, quantity: int, reason: str = "release") -> bool:
    """
    Release previously reserved stock (e.g., when deleting order item).
    
    Args:
        db: Database session
        product_id: ID of the product
        quantity: Quantity to release
        reason: Reason for release
        
    Returns:
        True if release successful, False otherwise
    """
    if quantity <= 0:
        return False
    
    product = db.get(Product, product_id)
    if not product:
        return False
    
    # Release the stock
    product.stock_reserved = max(0, product.stock_reserved - quantity)
    
    # Record the movement
    movement = StockMovement(
        product_id=product_id,
        qty_change=-quantity,
        reason=reason,
        notes=f"Released {quantity} units"
    )
    db.add(movement)
    
    db.commit()
    db.refresh(product)
    
    return True


def adjust_stock_on_hand(db: Session, product_id: int, adjustment: int, reason: str = "manual_adjust", notes: str = None) -> bool:
    """
    Manually adjust stock on hand (admin/manager only).
    
    Args:
        db: Database session
        product_id: ID of the product
        adjustment: Positive for addition, negative for reduction
        reason: Reason for adjustment
        notes: Additional notes
        
    Returns:
        True if adjustment successful, False otherwise
    """
    if adjustment == 0:
        return False
    
    product = db.get(Product, product_id)
    if not product:
        return False
    
    # Check if reduction would make stock negative
    if adjustment < 0 and (product.stock_on_hand + adjustment) < 0:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot reduce stock below 0. Current: {product.stock_on_hand}, Reduction: {abs(adjustment)}"
        )
    
    # Adjust the stock
    product.stock_on_hand += adjustment
    
    # Record the movement
    movement = StockMovement(
        product_id=product_id,
        qty_change=adjustment,
        reason=reason,
        notes=notes or f"Manual adjustment: {adjustment:+d}"
    )
    db.add(movement)
    
    db.commit()
    db.refresh(product)
    
    return True


def get_stock_status(db: Session, product_id: int) -> Optional[dict]:
    """
    Get current stock status for a product.
    
    Args:
        db: Database session
        product_id: ID of the product
        
    Returns:
        Dictionary with stock information
    """
    product = db.get(Product, product_id)
    if not product:
        return None
    
    return {
        "product_id": product_id,
        "stock_on_hand": product.stock_on_hand,
        "stock_reserved": product.stock_reserved,
        "available": product.stock_on_hand - product.stock_reserved
    }
