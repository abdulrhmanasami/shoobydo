#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8805}"
OUTDIR="reports/EPIC-02/TASK-02B"
OUT="$OUTDIR/DELIVERABLES.md"
mkdir -p "$OUTDIR"

# جمع أدلة
curl --max-time 5 --connect-timeout 2 -f -L -i "http://127.0.0.1:${PORT}/api/v1/suppliers/" \
  > "$OUTDIR/curl_01_list.txt" || true
curl --max-time 5 --connect-timeout 2 -f -L -i "http://127.0.0.1:${PORT}/openapi.json" \
  | jq -r '.paths | keys[]' | grep suppliers > "$OUTDIR/available_paths.txt" || true
LOG=$(ls -1t logs/backend-*.log | head -n1)
tail -n 200 "$LOG" > "$OUTDIR/backend_last200.log" || true

# توليد MD
{
  echo "# EPIC-02 / TASK-02B — Deliverables"
  echo "## 1) suppliers list (HTTP head)"
  echo '```'; sed -n '1,40p' "$OUTDIR/curl_01_list.txt"; echo '```'
  echo "## 2) available_paths (suppliers)"
  echo '```'; sed -n '1,40p' "$OUTDIR/available_paths.txt"; echo '```'
  echo "## 3) backend log tail (last 200)"
  echo '```'; sed -n '1,200p' "$OUTDIR/backend_last200.log"; echo '```'
} > "$OUT"
echo "✅ $OUT"
