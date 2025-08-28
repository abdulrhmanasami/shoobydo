from fastapi import APIRouter, Depends
from .routers import auth, suppliers, products, customers, orders, inventory, reports
from .security import get_current_user

def build_api_v1() -> APIRouter:
    api_v1 = APIRouter(prefix="/api/v1")
    # عامة
    api_v1.include_router(auth.router, tags=["auth"])
    # محمية
    protected = APIRouter(dependencies=[Depends(get_current_user)])
    protected.include_router(suppliers.router, tags=["suppliers"])
    protected.include_router(products.router,  tags=["products"])
    protected.include_router(customers.router, tags=["customers"])
    protected.include_router(orders.router,    tags=["orders"])
    protected.include_router(inventory.router, tags=["inventory"])
    protected.include_router(reports.router,   tags=["reports"])
    api_v1.include_router(protected)
    return api_v1
