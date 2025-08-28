#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../apps/backend"
# set -a && . ../.env.isolated && set +a  # Load env if exists
pkill -f "uvicorn .*apps\.backend\.app\.main:app" 2>/dev/null || true
rm -f /tmp/shoobydo-api.{pid,log}
source .venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port "${BACKEND_PORT:-8807}" >/tmp/shoobydo-api.log 2>&1 & echo $! >/tmp/shoobydo-api.pid
