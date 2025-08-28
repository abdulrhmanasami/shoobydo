#!/usr/bin/env bash
set -euo pipefail
. .env.dev
mkdir -p reports
ts=$(date +"%Y%m%d-%H%M%S")
for ep in "/health" "/reports/summary" "/reports/kpis" "/db/ping" "/cache/ping"; do
  curl -fsS "http://127.0.0.1:$PORT$ep" | tee "reports$(echo $ep | tr '/' '_')_${ts}.json" >/dev/null
done
echo "[smoke] written under reports/"
