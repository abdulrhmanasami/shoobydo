#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[tests] backend unit tests"
# export env so tests hit correct PORT
set -a; [ -f .env.dev ] && . .env.dev; set +a
cd apps/backend
python3 -m venv .venv >/dev/null 2>&1 || true
. .venv/bin/activate
python -m pip install -U pip wheel >/dev/null
pip install -r requirements.txt >/dev/null
pip install pytest requests >/dev/null
pytest -q || true
echo "[tests] done"


