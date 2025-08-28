import os
# Guard against accidentally importing a quarantined root "app"
assert not os.path.isdir(os.path.join(os.path.dirname(__file__), "../../.quarantine/root-app-dup")), \
    "Quarantined root app/ detected; remove ambiguity before running."

from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth
from app.routers.products import router as products
from app.routers.customers import router as customers
from app.routers.orders import router as orders
from app.routers.order_items import router as order_items
from app.routers.suppliers import router as suppliers
from app.routers.reports import router as reports
from app.routers.inventory import router as inventory
from app.security import get_current_user, require_role

app = FastAPI(title="Shoobydo API", version="0.2.x")

# disable auto slash redirects (prevents 307 spam)
app.router.redirect_slashes = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# تجميع النسخة /api/v1
api_v1 = APIRouter(prefix="/api/v1")

# مسارات عامة (Auth)
api_v1.include_router(auth, prefix="/auth", tags=["auth"])

# مسارات محمية بجلسة مصادق عليها
protected = APIRouter(dependencies=[Depends(get_current_user)])
protected.include_router(suppliers, tags=["suppliers"])
protected.include_router(products, tags=["products"])
protected.include_router(customers, tags=["customers"])
protected.include_router(orders, tags=["orders"])
protected.include_router(order_items, tags=["order_items"])
protected.include_router(inventory, tags=["inventory"])
protected.include_router(reports, tags=["reports"])

# تركيب /api/v1
api_v1.include_router(protected)

@app.get("/health", tags=["health"])
def root_health():
    return {"status":"ok"}

@app.get("/api/health", tags=["health"], include_in_schema=False)
def api_health():
    return {"status":"ok"}

app.include_router(api_v1)
