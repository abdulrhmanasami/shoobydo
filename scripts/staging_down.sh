#!/bin/bash
set -euo pipefail
docker compose -f docker-compose.staging.yml --env-file .env.staging down || true
pkill -f "uvicorn .*app\.main:app" || true
rm -f /tmp/shoobydo-api.{pid,log} || true
echo "✅ staging down"
