#!/bin/bash
set -euo pipefail
export COMPOSE_DOCKER_CLI_BUILD=1
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d
# انتظار الصحة (Rule D)
ok=0; for i in {1..120}; do
  docker compose -f docker-compose.staging.yml ps --status=running >/dev/null 2>&1 || true
  curl -sSfL --max-time 5 --connect-timeout 2 http://127.0.0.1:8801/health >/dev/null && ok=1 && break || sleep 2
done
[ "$ok" = 1 ] || { echo "❌ backend not healthy"; docker compose -f docker-compose.staging.yml logs backend | tail -n 160; exit 1; }
echo "✅ staging up ok"
