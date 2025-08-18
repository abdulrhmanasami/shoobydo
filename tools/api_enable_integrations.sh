#!/usr/bin/env bash
set -euo pipefail
root="$(pwd)"

# 1) تأمين المتطلبات (redis, psycopg2-binary, pandas, openpyxl)
req="$root/apps/backend/requirements.txt"
mkdir -p "$root/apps/backend"
touch "$req"
add() { grep -Eqi "^$1([=>< ]|$)" "$req" || echo "$2" >> "$req"; }
add "redis"               "redis>=5.0.0"
add "psycopg2-binary"     "psycopg2-binary>=2.9.9"
add "pandas"              "pandas>=2.2.0"
add "openpyxl"            "openpyxl>=3.1.2"

# 2) إضافة نقاط نهاية: /db/ping و /cache/ping و /reports/kpis (بدون لمس الموجود)
main="$root/apps/backend/app/main.py"
[ -f "$main" ] || { echo "ERROR: $main غير موجود"; exit 1; }

if ! grep -q "@app.get(\"/db/ping\"" "$main"; then
  cat >> "$main" <<'PY'

# === Integrations: DB/Redis/KPIs ===
from typing import Optional
from pydantic import BaseModel
import os

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
PY
fi

echo "[ok] API integrations appended"
