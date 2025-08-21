#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${PORT:-8805}"
PID_FILE="$ROOT/.run/uvicorn.pid"

if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE" || true)"
  if [ -n "${PID:-}" ] && ps -p "$PID" >/dev/null 2>&1; then
    kill -TERM "$PID" || true
    for i in {1..10}; do
      ps -p "$PID" >/dev/null 2>&1 || break
      sleep 0.5
    done
    ps -p "$PID" >/dev/null 2>&1 && kill -KILL "$PID" || true
  fi
  rm -f "$PID_FILE"
fi

# تنظيف منفذ عالق
lsof -ti :"$PORT" >/dev/null 2>&1 && kill -KILL $(lsof -ti :"$PORT") || true
echo "OK: backend stopped on :$PORT"
