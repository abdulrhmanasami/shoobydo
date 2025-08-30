#!/bin/bash
set -euo pipefail
B=${1:-http://127.0.0.1:8001}
TOK=${TOKEN:-}
H=()
[ -n "${TOK}" ] && H=(-H "Authorization: Bearer ${TOK}")
curl -sSfL --max-time 5 --connect-timeout 2 "$B/health" >/dev/null
curl -sSfL --max-time 5 --connect-timeout 2 "$B/openapi.json" | jq '.info.version' >/dev/null
for p in "/api/v1/reports/summary" "/api/v1/reports/kpis" "/api/v1/inventory/products" "/api/v1/suppliers" "/api/v1/admin/ping"; do
  if [ ${#H[@]} -eq 0 ]; then
    curl -sS -f -L --max-time 5 --connect-timeout 2 "$B$p" >/dev/null || echo "[WARN] $p guarded (expected 401/403/404)"
  else
    curl -sS -f -L --max-time 5 --connect-timeout 2 "${H[@]}" "$B$p" >/dev/null || echo "[WARN] $p guarded (expected 401/403/404)"
  fi
done
echo "OK"
