#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

OUT="final_docs_$(date +%Y%m%d).zip"
zip -r "$OUT" docs/ apps/frontend/public/logo.png -x "**/node_modules/**" >/dev/null
echo "Created $OUT"
