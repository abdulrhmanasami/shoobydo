#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8805}"
OUTDIR="reports/EPIC-02/TASK-02B"; mkdir -p "$OUTDIR"
LIST="$OUTDIR/curl_01_list.txt"
PATHS="$OUTDIR/available_paths.txt"
LOGF="$OUTDIR/backend_last200.log"
OUT="$OUTDIR/DELIVERABLES.md"

curl --max-time 5 --connect-timeout 2 -f -L -i "http://127.0.0.1:${PORT}/api/v1/suppliers/" > "$LIST" || true
curl --max-time 5 --connect-timeout 2 -f -L -s "http://127.0.0.1:${PORT}/openapi.json" \
 | jq -r '.paths | keys[]' | grep suppliers > "$PATHS" || true
LOG="$(ls -1t logs/backend-*.log | head -n1)"; tail -n 200 "$LOG" > "$LOGF" || true

{
  echo "# EPIC-02 / TASK-02B — Deliverables"
  echo "## 1) suppliers list (HTTP head)"; echo '```'; sed -n '1,40p' "$LIST"; echo '```'
  echo "## 2) available_paths (suppliers)"; echo '```'; sed -n '1,60p' "$PATHS"; echo '```'
  echo "## 3) backend log tail (last 200)"; echo '```'; sed -n '1,200p' "$LOGF"; echo '```'
} > "$OUT"
echo "✅ $OUT"
