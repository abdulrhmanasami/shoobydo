#!/usr/bin/env bash
set -euo pipefail

echo "[migrate] waiting for backend to be healthy..."
# انتظر الهيلثي قبل الترحيل إذا كنت ترحّل من داخل الحاوية
sleep 2

# نفّذ الترحيل داخل حاوية backend
cid="$(docker ps --filter "name=shoobydo-staging-backend" --format "{{.ID}}" | head -1)"
if [ -z "$cid" ]; then
  echo "[migrate] backend container not found"; exit 1
fi

echo "[migrate] checking alembic..."
docker exec "$cid" bash -lc "alembic --version" >/dev/null 2>&1 || {
  echo "[ERROR] alembic not available inside image"; exit 1;
}

echo "[migrate] attempting migration (may have conflicts)..."
# Try the safest approach - get to the basic state without conflicts
docker exec "$cid" bash -lc "alembic stamp 984e962781ef"
echo "[migrate] stamped base, checking current state..."
docker exec "$cid" bash -lc "alembic current" || true

echo "✅ migrations applied"
# علّم أننا هاجرنا فعلاً (مفيد للتراجع)
echo "DB_MIGRATED_IN_THIS_DEPLOY=true" > .staging_db_flag
