#!/usr/bin/env bash
set -euo pipefail
source .env.dev
mkdir -p reports
health=$(ls -t reports/health_*.json | head -n1)
summary=$(ls -t reports/summary_*.json | head -n1)
sup=$(python3 - <<PY "$summary"
import json,sys
d=json.load(open(sys.argv[1]))
print(d.get("suppliers") or d.get("Suppliers") or 0)
PY
)
ts=$(date +"%Y%m%d-%H%M%S")
cat > "reports/STATUS_$ts.md" <<MD
# Shoobydo — Quick Status ($ts)
- **PORT:** $PORT
- **Postgres:** $POSTGRES_PORT
- **Redis:** $REDIS_PORT
- **Health:** $(basename "$health")
- **Summary:** $(basename "$summary")
- **Suppliers:** $sup
MD
echo "[written] reports/STATUS_$ts.md"
