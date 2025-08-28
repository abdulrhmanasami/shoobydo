#!/bin/bash
# tools/make_02J_deliverables.sh
set -euo pipefail
PORT="${PORT:-8805}"
OUTDIR="reports/EPIC-02/TASK-02J"
OUT="$OUTDIR/DELIVERABLES.md"
mkdir -p "$OUTDIR"

{
  echo "# EPIC-02 / TASK-02J — Deliverables"
  echo
  echo "## 1) head -n 40 curl_01_add_items.txt"
  echo '```'
  if [ -s "$OUTDIR/curl_01_add_items.txt" ]; then
    head -n 40 "$OUTDIR/curl_01_add_items.txt"
  else
    echo "(ملف curl_01_add_items.txt غير موجود أو فارغ)"
  fi
  echo '```'
  echo
  echo "## 2) available_paths (أول 30 سطر)"
  echo '```'
  if [ -s "$OUTDIR/available_paths.txt" ]; then
    sed -n '1,30p' "$OUTDIR/available_paths.txt"
  else
    # إعادة توليدها من الـ OpenAPI لو احتجت
    curl -s "http://127.0.0.1:${PORT}/openapi.json" | jq -r '.paths | keys[]' | sort | sed -n '1,30p'
  fi
  echo '```'
  echo
  echo "## 3) PR link"
  echo '```'
  if [ -s "$OUTDIR/pr_link.txt" ]; then
    cat "$OUTDIR/pr_link.txt"
  else
    echo "(pr_link.txt غير موجود — ضع رابط الـ PR هنا)"
  fi
  echo '```'
  echo
  echo "—"
  echo "ENV: PORT=${PORT}"
  echo "Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'n/a')"
  echo "Health: $(curl -sf -m 3 "http://127.0.0.1:${PORT}/api/health" 2>/dev/null || echo 'unreachable')"
} > "$OUT"

echo "✅ جاهز: $OUT"
