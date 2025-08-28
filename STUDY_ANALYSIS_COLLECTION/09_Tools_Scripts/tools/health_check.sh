#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .env.dev
mkdir -p reports
ts=$(date +"%Y%m%d-%H%M%S")
curl -s "http://127.0.0.1:$PORT/health" | tee "reports/health_${ts}.json" >/dev/null
curl -s "http://127.0.0.1:$PORT/reports/summary" | tee "reports/summary_${ts}.json" >/dev/null
echo "[written] reports/health_${ts}.json  reports/summary_${ts}.json"

