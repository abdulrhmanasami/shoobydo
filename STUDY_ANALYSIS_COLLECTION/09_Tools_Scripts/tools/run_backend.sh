#!/usr/bin/env bash
set -euo pipefail
cd "${BASH_SOURCE%/*}/.."  # repo root
[ -d apps/backend/app ] || { echo "❌ apps/backend/app missing"; exit 1; }
cd apps/backend
[ -f .venv/bin/activate ] || { echo "❌ .venv missing; run: python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt"; exit 1; }
source .venv/bin/activate
nohup uvicorn app.main:app --host 127.0.0.1 --port "${PORT:-8807}" > /tmp/shoobydo-api.log 2>&1 & echo $! >/tmp/shoobydo-api.pid
for i in {1..30}; do
  curl -f -L --max-time 5 --connect-timeout 2 "http://127.0.0.1:${PORT:-8807}/health" >/dev/null && exit 0
  sleep 1
done
echo "health timeout"; tail -n 120 /tmp/shoobydo-api.log; exit 1
