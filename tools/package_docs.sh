#!/usr/bin/env bash
python3 tools/linkify_docs_readme.py >/dev/null 2>&1 || true
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

OUT="final_docs_$(date +%Y%m%d).zip"
zip -r "$OUT" docs/ apps/frontend/public/logo.png -x "**/node_modules/**" >/dev/null
echo "Created $OUT"
