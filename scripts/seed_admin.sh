#!/usr/bin/env bash
set -euo pipefail
API_URL="${API_URL:-http://127.0.0.1:8001}"
EMAIL="${ADMIN_EMAIL:-admin@example.com}"
PASS="${ADMIN_PASSWORD:-Passw0rd!}"

echo "[seed] login..."
TOKEN="$(curl -s -X POST "$API_URL/api/v1/login" -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" | jq -r '.access_token // empty' || true)"

if [ -z "$TOKEN" ]; then
  echo "[seed] register..."
  curl -s -X POST "$API_URL/api/v1/register" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" >/dev/null || true

  TOKEN="$(curl -s -X POST "$API_URL/api/v1/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" | jq -r '.access_token // empty' || true)"
fi

test -n "$TOKEN" || { echo "[seed] no token, check logs"; exit 1; }

echo "[seed] verify protected endpoints..."
curl -sf -H "Authorization: Bearer $TOKEN" "$API_URL/api/v1/admin/ping" >/dev/null && echo "✓ admin/ping"
curl -sf -H "Authorization: Bearer $TOKEN" "$API_URL/api/v1/reports/"   >/dev/null && echo "✓ reports/"
echo "[seed] done."
