#!/usr/bin/env bash
set -euo pipefail
. .env.dev
mkdir -p reports
ts=$(date +"%Y%m%d-%H%M%S")
health=$(ls -t reports/health_*.json 2>/dev/null | head -n1)
summary=$(ls -t reports/summary_*.json 2>/dev/null | head -n1)
dhealth=$(ls -t reports/health_docker_*.json 2>/dev/null | head -n1)
dsummary=$(ls -t reports/summary_docker_*.json 2>/dev/null | head -n1)
sup=$(python3 - <<PY "$summary"
import json,sys; d=json.load(open(sys.argv[1])) if sys.argv[1] else {}; print(d.get("suppliers") or d.get("Suppliers") or 0)
PY
)
cat > "reports/FINAL_STATUS_$ts.md" <<MD
# Shoobydo — Final Status ($ts)
- PORT: 8801
- Postgres: 
- Redis: 
- FRONTEND_PORT: N/A

## Host
- Health: A
- Summary: A

## Docker
- Health: A
- Summary: A

**Suppliers (after fix):** 
MD
