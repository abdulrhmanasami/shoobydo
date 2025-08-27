#!/usr/bin/env bash
set -euo pipefail
base="http://127.0.0.1:8000"
probe() { path="$1"; code=$(curl -s -o /dev/null -w "%{http_code}" -f -L --max-time 5 --connect-timeout 2 "$base$path" || true); printf "%-28s %s\n" "$path" "$code"; }
declare -a paths=( "/health" "/api/v1/reports/summary" "/api/v1/inventory/products/1/stock" "/api/v1/products/" "/api/v1/orders/" "/api/v1/suppliers" "/api/v1/customers/" )
for p in "${paths[@]}"; do probe "$p"; done
