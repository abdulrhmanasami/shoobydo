#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8805}"
OUTDIR="reports/EPIC-02/TASK-02D"; mkdir -p "$OUTDIR"
LIST_U="$OUTDIR/01_get_suppliers_user.txt"
POST_U="$OUTDIR/02_post_supplier_user.txt"
POST_A="$OUTDIR/03_post_supplier_admin.txt"
PATHS="$OUTDIR/available_paths.txt"
LOGF="$OUTDIR/backend_last200.log"
OUT="$OUTDIR/DELIVERABLES.md"

. tools/scurl.sh

ADM="$(scurl -s -X POST "http://127.0.0.1:$PORT/api/v1/auth/login" -H 'Content-Type: application/json' -d '{"email":"admin@example.com","password":"admin123"}' | jq -r .access_token)"
USR_EMAIL="user$(date +%s)@ex.com"; export USR_EMAIL; python3 - <<'PY'
import os
os.environ.setdefault("POSTGRES_PORT","5547")
from app.db import SessionLocal
from app.models_user import User, UserRole
from app.security import hash_password
db=SessionLocal()
u=User(email=os.environ["USR_EMAIL"], password_hash=hash_password("user123"), role=UserRole.viewer)
db.add(u); db.commit()
print("user seed ok")
PY
USR="$(scurl -s -X POST "http://127.0.0.1:$PORT/api/v1/auth/login" -H 'Content-Type: application/json' -d "{\"email\":\"$USR_EMAIL\",\"password\":\"user123\"}" | jq -r .access_token)"

scurl -i "http://127.0.0.1:$PORT/api/v1/suppliers/" -H "Authorization: Bearer $USR" > "$LIST_U" || true
scurl -i -X POST "http://127.0.0.1:$PORT/api/v1/suppliers/" -H "Authorization: Bearer $USR" -H 'Content-Type: application/json' \
  -d '{"name":"RBAC USER BLOCK","file_path":"/block.xlsx","rows":1,"sheets":1}' > "$POST_U" || true
scurl -i -X POST "http://127.0.0.1:$PORT/api/v1/suppliers/" -H "Authorization: Bearer $ADM" -H 'Content-Type: application/json' \
  -d '{"name":"RBAC ADMIN OK","file_path":"/ok.xlsx","rows":2,"sheets":1}' > "$POST_A" || true

curl --max-time 5 --connect-timeout 2 -fsL "http://127.0.0.1:$PORT/openapi.json" | jq -r '.paths | keys[]' | sort > "$PATHS" || true
LOG="$(ls -1t logs/backend-*.log | head -n1)"; tail -n 200 "$LOG" > "$LOGF" || true

{
  echo "# EPIC-02 / TASK-02D — Auth/RBAC Deliverables"
  echo "## 1) GET /suppliers/ (user)"; echo '```'; sed -n '1,25p' "$LIST_U"; echo '```'
  echo "## 2) POST /suppliers/ (user → 403)"; echo '```'; sed -n '1,25p' "$POST_U"; echo '```'
  echo "## 3) POST /suppliers/ (admin → 200)"; echo '```'; sed -n '1,25p' "$POST_A"; echo '```'
  echo "## 4) available_paths"; echo '```'; sed -n '1,60p' "$PATHS"; echo '```'
  echo "## 5) backend log tail"; echo '```'; sed -n '1,200p' "$LOGF"; echo '```'
} > "$OUT"
echo "✅ $OUT"
