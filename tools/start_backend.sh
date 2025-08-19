#!/usr/bin/env bash
set -euo pipefail

# Ensure we run from repo root
cd "$(dirname "$0")/.."

# Load env and sanitize
if [ -f .env.dev ]; then
  set -a; . .env.dev; set +a
fi
PORT=${PORT:-}
PORT=$(printf "%s" "$PORT" | tr -d '\r')
if [ -z "$PORT" ]; then PORT=8800; fi

MODE="docker"; [ -f .backend_mode ] && MODE=$(cat .backend_mode)

is_healthy(){ curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; }

if [ "$MODE" = "docker" ]; then
  if is_healthy; then
    echo "[backend] docker healthy on :$PORT (skip local)"
    exit 0
  fi
  echo "[backend] docker not healthy; falling back to local"
fi

cd apps/backend
. .venv/bin/activate 2>/dev/null || (python3 -m venv .venv && . .venv/bin/activate)
python -m pip install -U pip wheel >/dev/null
[ -f requirements.txt ] && pip install -r requirements.txt >/dev/null || pip install fastapi uvicorn[standard] jinja2 pydantic python-multipart >/dev/null

lsof -ti :"$PORT" | xargs -r kill -9 || true
nohup uvicorn app.main:app --host 127.0.0.1 --port "$PORT" --reload > "/tmp/uvicorn.$PORT.log" 2>&1 & echo $! > "/tmp/uvicorn.$PORT.pid"
sleep 2
tail -n 20 "/tmp/uvicorn.$PORT.log" || true
