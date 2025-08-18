#!/usr/bin/env bash
set -euo pipefail
./tools/no_conflict.sh
. .env.dev
echo "docker" > .backend_mode

mkdir -p apps/frontend/public
ln -snf ../../docs   apps/frontend/public/docs
ln -snf ../../assets apps/frontend/public/assets
ln -snf ../../data   apps/frontend/public/data

cd infra
COMPOSE_PROJECT_NAME="${APP_NAMESPACE:-shoobydo}" docker compose --env-file ../.env.dev up -d db redis backend
docker compose ps
cd ..

for i in {1..30}; do
  curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null && break || sleep 1
done

tools/health_check.sh || true
tools/quick_report.sh || true
tools/final_status.sh  || true
echo "[dev_up] done"
