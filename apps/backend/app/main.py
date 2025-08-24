from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, customers, orders, order_items, suppliers

app = FastAPI(title="Shoobydo API", version="0.2.x")

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
api_v1.include_router(suppliers,    prefix="/suppliers",  tags=["suppliers"])

@app.get("/api/health")
def health():
    return {"ok": True}

app.include_router(api_v1)
