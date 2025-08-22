#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${PORT:-8805}"
LOG_DIR="$ROOT/logs"; RUN_DIR="$ROOT/.run"
mkdir -p "$LOG_DIR" "$RUN_DIR"
cd "$ROOT/apps/backend"

[ -x .venv/bin/python ] || python3 -m venv .venv
. .venv/bin/activate

# مبدئيًا إن وُجد Alembic
command -v alembic >/dev/null 2>&1 && alembic upgrade head || true

# حرّر المنفذ
if lsof -ti :"$PORT" >/dev/null 2>&1; then
  kill $(lsof -ti :"$PORT") || true
  sleep 1
fi

TS="$(date +%Y%m%d-%H%M%S)"
LOG="$LOG_DIR/backend-$TS.log"

nohup .venv/bin/python -m uvicorn app.main:app \
  --host 0.0.0.0 --port "$PORT" --no-access-log \
  >>"$LOG" 2>&1 & echo $! > "$RUN_DIR/uvicorn.pid"

sleep 3
curl --max-time 5 --connect-timeout 2 -fsSL "http://127.0.0.1:${PORT}/openapi.json" >/dev/null || echo "WARN: OpenAPI not responding. See $LOG"
echo "OK: uvicorn pid=$(cat "$RUN_DIR/uvicorn.pid"), log=$LOG"
