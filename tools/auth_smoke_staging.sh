#!/usr/bin/env bash
set -euo pipefail

BASE="${STAGING_BASE_URL:-http://127.0.0.1:8802}"
EMAIL="${ADMIN_EMAIL:-admin@example.com}"
PASS="${ADMIN_PASSWORD:-ChangeMe123}"

echo "[auth] login..."
RESP="$(curl -sS -X POST "$BASE/api/v1/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}")"

# حاول jq، وإلا استخرج بالتعبيرات
if command -v jq >/dev/null 2>&1; then
  TOKEN="$(printf '%s' "$RESP" | jq -r '.access_token // empty')"
else
  TOKEN="$(printf '%s' "$RESP" | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')"
fi

if [ -z "${TOKEN:-}" ]; then
  echo "[auth] FAILED to obtain token"; echo "$RESP"; exit 1
fi
echo "[auth] got token: ${#TOKEN} chars"

auth_get() {
  local path="$1"
  code=$(curl -sS -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $TOKEN" "$BASE$path")
  echo "[${code}] GET $path"
  [ "$code" -eq 200 ] || exit 2
}

# اختبارات أمثلة — عدّل المسارات حسب مشروعك
auth_get "/api/v1/reports/summary"
auth_get "/api/v1/reports/kpis"

echo "✅ auth smoke passed"
