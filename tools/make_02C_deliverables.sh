#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8805}"
OUTDIR="reports/EPIC-02/TASK-02C"; mkdir -p "$OUTDIR"
PATHS="$OUTDIR/available_paths.txt"
LOGF="$OUTDIR/backend_last200.log"
OUT="$OUTDIR/DELIVERABLES.md"

curl --max-time 5 --connect-timeout 2 -f -L -s "http://127.0.0.1:${PORT}/openapi.json" \
 | jq -r '.paths | keys[]' | grep -E '^/api/v1/orders' | sort > "$PATHS" || echo "No orders paths found" > "$PATHS"
LOG="$(ls -1t logs/backend-*.log | head -n1)"; tail -n 200 "$LOG" > "$LOGF" || true

{
  echo "# EPIC-02 / TASK-02C — Deliverables"
  echo "## 1) available_paths (orders)"; echo '```'; sed -n '1,60p' "$PATHS"; echo '```'
  echo "## 2) backend log tail (last 200)"; echo '```'; sed -n '1,200p' "$LOGF"; echo '```'
} > "$OUT"
echo "✅ $OUT"
