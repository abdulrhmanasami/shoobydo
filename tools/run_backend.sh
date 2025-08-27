#!/usr/bin/env bash
set -euo pipefail
pkill -f "uvicorn .*app\.main:app" || true
rm -f /tmp/shoobydo-api.{pid,log}
cd apps/backend
nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 \
  > /tmp/shoobydo-api.log 2>&1 & echo $! > /tmp/shoobydo-api.pid
for i in {1..30}; do
  curl -f -L --max-time 5 --connect-timeout 2 http://127.0.0.1:8000/health >/dev/null && exit 0
  sleep 1
done
echo "health timeout"; tail -n 120 /tmp/shoobydo-api.log; exit 1
