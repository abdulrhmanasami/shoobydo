from app.routers import inventory, reports
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth
from app.routers.products import router as products
from app.routers.customers import router as customers
from app.routers.orders import router as orders
from app.routers.order_items import router as order_items
from app.routers.suppliers import router as suppliers

app = FastAPI(title="Shoobydo API", version="0.2.x")

# prevent implicit 307 redirects
try:
    app.router.redirect_slashes = False
except Exception:
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

api_v1 = APIRouter(prefix="/api/v1")

# ملاحظة: في __init__.py صدّرنا كائن router مباشرةً، لذلك نمرّره كما هو.
api_v1.include_router(auth,        prefix="/auth",         tags=["auth"])
api_v1.include_router(products,                         tags=["products"])
api_v1.include_router(customers,                        tags=["customers"])
api_v1.include_router(orders,                           tags=["orders"])
api_v1.include_router(order_items,                      tags=["order_items"])
api_v1.include_router(suppliers, prefix="/suppliers", tags=["suppliers"])

@app.get("/health", tags=["health"])
def root_health():
    return {"status":"ok"}

@app.get("/api/health", tags=["health"], include_in_schema=False)
def api_health():
    return {"status":"ok"}

app.include_router(api_v1)

api_v1.include_router(inventory, prefix='/inventory', tags=['inventory'])

api_v1.include_router(reports, prefix='/reports', tags=['reports'])
