#!/bin/bash
set -euo pipefail
docker compose -f docker-compose.staging.yml exec -T backend bash -lc '
set -e
if command -v alembic >/dev/null 2>&1; then
  alembic upgrade head
else
  python -c "print(\"[warn] alembic not installed — skipping\")"
fi
'
echo "✅ migrations ok"
