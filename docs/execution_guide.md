# Execution Guide

## Local Setup
- Requirements: Python 3.11+, Node 18+, Docker (optional), Git
- Env: `.env.dev` contains PORT/POSTGRES_/REDIS_/FRONTEND_PORT per no-conflict policy

### Bring up dev stack
- `tools/dev_up.sh` → picks free ports, starts db/redis/backend, health reports
- Backend (local): `tools/start_backend.sh` (respects `.backend_mode`)
- Frontend: `tools/start_frontend.sh`

### Testing & Reports
- Backend tests: `tools/run_tests.sh` (pytest)
- Health & summaries: `tools/health_check.sh`, `tools/quick_report.sh`, `tools/final_status.sh`

### Data & Suppliers
- Reindex from Excel: `POST /suppliers/reindex`
- Upload Excel: UI `/upload` or `POST /suppliers/upload`

## Production Notes (high-level)
- Containerize backend (Dockerfile exists) and serve via ASGI (Uvicorn or Gunicorn/Uvicorn workers)
- Persist Postgres volume, managed Redis
- CI/CD: build, run tests, deploy containers, run Alembic `upgrade head`

### Deployment steps (example: single VPS with Docker Compose)
1) Copy repo to server and set `.env.prod` with ports from no‑conflict policy
2) `docker compose -f infra/docker-compose.yml -f infra/docker-compose.override.yml --profile with-redis up -d db redis backend`
3) Run DB migrations: `docker compose exec backend alembic upgrade head`
4) Put reverse proxy (Caddy/NGINX) in front of backend and Next.js
5) Monitoring: enable health endpoints `/health`, `/reports/summary`, logs shipping

## Roles & Daily Routines
- Developer: implement endpoints/UI, run tests, update Alembic, review logs
- Operator: monitor health, refresh KPIs, manage suppliers uploads, review errors
- Marketer: use templates under `docs/templates/marketing/`, track KPIs in `docs/kpi_targets.md`

## Troubleshooting
- Port conflicts: re-run `tools/no_conflict.sh` and restart services
- DB migrations: `apps/backend/.venv/bin/alembic upgrade head`
- Frontend port busy: kill pid file `/tmp/next.$PORT.pid` or re-run start script
