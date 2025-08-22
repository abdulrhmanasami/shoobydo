from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# استيراد الراوترات كوحدات، لمرة واحدة فقط
from app.routers import auth, products, customers, orders, order_items

app = FastAPI(title="Shoobydo API", version="0.1.0")

# CORS أساسي (اختياري آمن)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# توحيد الـprefix: /api/v1
api_v1 = APIRouter(prefix="/api/v1")

# ملاحظة:
# - products/customers/orders/order_items لديهم غالبًا prefix داخلي (مثل "/products")
#   لذا نضمّنهم كما هم (بدون prefix إضافي هنا).
# - auth غالبًا بلا prefix داخلي، فنضيف له "/auth".
api_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1.include_router(products.router, tags=["products"])
api_v1.include_router(customers.router, tags=["customers"])
api_v1.include_router(orders.router, tags=["orders"])
api_v1.include_router(order_items.router, tags=["order_items"])

# تجميع تحت التطبيق
app.include_router(api_v1)

# Health واضح وثابت
@app.get("/api/health")
def health():
    return {"status": "ok"}
