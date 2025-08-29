#!/usr/bin/env bash
set -euo pipefail
APP_NAMESPACE=${APP_NAMESPACE:-shoobydo}
pick_free(){ local p=$1; while lsof -ti :"$p" >/dev/null 2>&1; do p=$((p+1)); done; echo "$p"; }

# read existing if present
[ -f .env.dev ] && source .env.dev || true

BACKEND_PORT=$(pick_free "${PORT:-8800}")
POSTGRES_PORT=$(pick_free "${POSTGRES_PORT:-5543}")
REDIS_PORT=$(pick_free "${REDIS_PORT:-6390}")

cat > .env.dev <<ENV
APP_NAMESPACE=$APP_NAMESPACE
COMPOSE_PROJECT_NAME=$APP_NAMESPACE
PORT=$BACKEND_PORT
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=$POSTGRES_PORT
POSTGRES_DB=eurodropship
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
REDIS_HOST=127.0.0.1
REDIS_PORT=$REDIS_PORT
ENV

echo "[no-conflict] namespace=$APP_NAMESPACE PORT=$BACKEND_PORT PG=$POSTGRES_PORT REDIS=$REDIS_PORT"

