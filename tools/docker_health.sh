#!/usr/bin/env bash
set -euo pipefail
. .env.dev
mkdir -p reports
ts=$(date +"%Y%m%d-%H%M%S")
cd infra
COMPOSE_PROJECT_NAME="${APP_NAMESPACE:-shoobydo}" docker compose ps | tee "../reports/compose_ps_$ts.txt" >/dev/null
cd ..
curl -s "http://127.0.0.1:$PORT/health" | tee "reports/health_docker_$ts.json" >/dev/null
curl -s "http://127.0.0.1:$PORT/reports/summary" | tee "reports/summary_docker_$ts.json" >/dev/null
echo "[docker_health] done"
