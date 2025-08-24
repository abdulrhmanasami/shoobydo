from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routers import suppliers  # تأكد من __init__.py

app = FastAPI(title="Shoobydo API", version="0.2.x")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(suppliers, prefix="/suppliers", tags=["suppliers"])

@app.get("/api/health")
def health():
    return {"ok": True}

app.include_router(api_v1)
