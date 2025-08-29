from fastapi import APIRouter, Depends
from .routers import auth, suppliers, products, customers, orders, order_items, inventory, reports, admin, _diag, health
from .security import get_current_user

def build_api_v1() -> APIRouter:
    api_v1 = APIRouter(prefix="/api/v1")

    # Health check موسّع
    api_v1.include_router(health.router, tags=["health"])

    # Canonical (بدون prefix: /api/v1/login, /register, /me, /logout)
    api_v1.include_router(auth.router, prefix="", tags=["auth"])
    api_v1.include_router(_diag.router)  # dev only

    # Alias: /api/v1/auth/* (مخفية عن الـ schema لتجنب ازدواجية التوثيق)
    api_v1.include_router(auth.router, prefix="/auth", tags=["auth"], include_in_schema=False)

    # Admin router (admin only)
    api_v1.include_router(admin.router, prefix="/admin", tags=["admin"])

    # باقي الروترات كما هي (لا تضف prefixes إضافية كي لا تتكرر القطاعات)
    protected = APIRouter(dependencies=[Depends(get_current_user)])
    for r in (suppliers.router, products.router, customers.router, orders.router, order_items.router, inventory.router, reports.router):
        protected.include_router(r)
    api_v1.include_router(protected)
    return api_v1
