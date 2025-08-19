from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

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

class ReportSummary(BaseModel):
    suppliers: int
    kpis: int
    notes: str

@app.get("/reports/summary", response_model=ReportSummary)
def reports_summary():
    import os
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
    suppliers = 0
    if os.path.isdir(data_dir):
        for root, _, files in os.walk(data_dir):
            suppliers += sum(1 for f in files if f.lower().endswith(".xlsx"))
    return ReportSummary(suppliers=suppliers, kpis=2, notes="based on Excel models")

# === Integrations: DB/Redis/KPIs ===
from typing import Optional
from pydantic import BaseModel
import os
from app.routers import suppliers
from app.routers import auth as auth_router
from app.routers import admin as admin_router
from app.schemas import CostsSummary

class KPISummary(BaseModel):
    files: int
    rows: int
    sheets: int
    notes: Optional[str] = None

@app.get("/db/ping")
def db_ping():
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST","127.0.0.1"),
            port=int(os.getenv("POSTGRES_PORT","5432")),
            dbname=os.getenv("POSTGRES_DB","postgres"),
            user=os.getenv("POSTGRES_USER","postgres"),
            password=os.getenv("POSTGRES_PASSWORD","postgres"),
            connect_timeout=2,
        )
        cur = conn.cursor()
        cur.execute("select version()")
        ver = cur.fetchone()[0]
        cur.close(); conn.close()
        return {"ok": True, "version": ver}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/cache/ping")
def cache_ping():
    try:
        import redis
        r = redis.Redis(
            host=os.getenv("REDIS_HOST","127.0.0.1"),
            port=int(os.getenv("REDIS_PORT","6379")),
            socket_connect_timeout=2,
        )
        pong = r.ping()
        return {"ok": bool(pong)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/reports/kpis", response_model=KPISummary)
def reports_kpis():
    # احصائيات سريعة من كل ملفات .xlsx في data/**
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
    files = []
    if os.path.isdir(data_dir):
        for root, _, fs in os.walk(data_dir):
            for f in fs:
                if f.lower().endswith(".xlsx"):
                    files.append(os.path.join(root, f))
    rows = 0
    sheets = 0
    try:
        import pandas as pd
        for f in files:
            try:
                xl = pd.ExcelFile(f)
                sheets += len(xl.sheet_names)
                for name in xl.sheet_names:
                    try:
                        df = xl.parse(name)
                        rows += int(df.shape[0])
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception as e:
        return KPISummary(files=len(files), rows=rows, sheets=sheets, notes=f"pandas/openpyxl issue: {e}")
    return KPISummary(files=len(files), rows=rows, sheets=sheets, notes="ok")

# Suppliers router
app.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(admin_router.router, prefix="/admin", tags=["admin"])


@app.get("/reports/costs", response_model=CostsSummary)
def reports_costs():
    """Summarize costs from data/02_Excel/suppliers_model_02.xlsx.
    Reads first sheet only; sums numeric columns heuristically.
    """
    data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "02_Excel", "suppliers_model_02.xlsx"))
    if not os.path.isfile(data_file):
        return CostsSummary(files=0, rows=0, total_cost=0.0, total_margin=0.0, notes="file not found")
    try:
        import pandas as pd
        xl = pd.ExcelFile(data_file)
        sheet = xl.sheet_names[0]
        df = xl.parse(sheet)
        rows = int(df.shape[0])
        lower_cols = {str(c).lower(): c for c in df.columns}
        total_cost = 0.0
        total_margin = 0.0
        if 'total_cost' in lower_cols:
            total_cost = float(pd.to_numeric(df[lower_cols['total_cost']], errors='coerce').fillna(0).sum())
        if 'total_margin' in lower_cols:
            total_margin = float(pd.to_numeric(df[lower_cols['total_margin']], errors='coerce').fillna(0).sum())
        if total_cost == 0.0:
            num_df = df.select_dtypes(include=['number'])
            total_cost = float(num_df.sum(numeric_only=True).sum()) if not num_df.empty else 0.0
        if total_margin == 0.0 and 'margin' in lower_cols:
            total_margin = float(pd.to_numeric(df[lower_cols['margin']], errors='coerce').fillna(0).sum())
        return CostsSummary(files=1, rows=rows, total_cost=round(total_cost,2), total_margin=round(total_margin,2), notes="ok")
    except Exception as e:
        return CostsSummary(files=1, rows=0, total_cost=0.0, total_margin=0.0, notes=f"pandas/openpyxl issue: {e}")
