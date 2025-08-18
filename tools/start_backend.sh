#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .env.dev
cd apps/backend
. .venv/bin/activate 2>/dev/null || (python3 -m venv .venv && . .venv/bin/activate)
python -m pip install -U pip wheel >/dev/null
if [ -f requirements.txt ]; then
  pip install -r requirements.txt >/dev/null
else
  pip install fastapi uvicorn[standard] jinja2 pydantic python-multipart >/dev/null
fi
lsof -ti :"$PORT" | xargs -r kill -9 || true
[ -f "/tmp/uvicorn.$PORT.pid" ] && kill -9 "$(cat "/tmp/uvicorn.$PORT.pid")" 2>/dev/null || true
nohup uvicorn app.main:app --host 127.0.0.1 --port "$PORT" --reload > "/tmp/uvicorn.$PORT.log" 2>&1 & echo $! > "/tmp/uvicorn.$PORT.pid"
sleep 2
tail -n 10 "/tmp/uvicorn.$PORT.log" || true

