#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT/.run"
if [[ -f "$RUN_DIR/uvicorn.pid" ]]; then
  PID="$(cat "$RUN_DIR/uvicorn.pid" || true)"
  if [[ -n "${PID:-}" ]] && ps -p "$PID" >/dev/null 2>&1; then
    kill "$PID" || true
  fi
  rm -f "$RUN_DIR/uvicorn.pid"
fi
echo "stopped"
