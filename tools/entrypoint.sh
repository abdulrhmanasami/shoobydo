#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Waiting for DB..."
python - <<'PY'
import os, time, sys
import psycopg2
dsn = "dbname={db} user={u} password={p} host={h} port={port}".format(
    db=os.getenv("POSTGRES_DB","postgres"),
    u=os.getenv("POSTGRES_USER","postgres"),
    p=os.getenv("POSTGRES_PASSWORD",""),
    h=os.getenv("POSTGRES_HOST","db"),
    port=os.getenv("POSTGRES_PORT","5432"),
)
for i in range(120):
    try:
        psycopg2.connect(dsn).close()
        sys.exit(0)
    except Exception:
        time.sleep(1)
print("DB not ready after 120s", file=sys.stderr); sys.exit(1)
PY

echo "[entrypoint] Applying migrations..."
alembic upgrade head || {
  echo "[entrypoint] No migrations found, generating initial migration..."
  alembic revision --autogenerate -m "0001_initial_schema"
  alembic upgrade head
}

echo "[entrypoint] Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
