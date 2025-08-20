from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from app.routers import suppliers
from app.routers import auth as auth_router
from app.routers import admin as admin_router
from app.routers import products as products_router
from app.routers import orders as orders_router
from app.routers import order_items as order_items_router

app = FastAPI(title="shoobydo-api")

# CORS for local frontend
import os as _os
_fe_port = _os.getenv("FRONTEND_PORT", "3000")
_origins = [f"http://127.0.0.1:{_fe_port}", f"http://localhost:{_fe_port}"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Existing endpoints below (trimmed for brevity) ...

# Routers
app.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(admin_router.router, prefix="/admin", tags=["admin"])
app.include_router(products_router.router, prefix="/products", tags=["products"])
app.include_router(orders_router.router, prefix="/orders", tags=["orders"])
app.include_router(order_items_router.router, tags=["orders"])
