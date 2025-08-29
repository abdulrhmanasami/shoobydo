SHELL := /bin/bash

.PHONY: dev-backend dev-frontend up down lint

dev-backend:
	cd apps/backend && . .venv/bin/activate && uvicorn app.main:app --reload --port ${PORT:-8800}

dev-frontend:
	cd apps/frontend && npm run dev

up:
	cd infra && docker compose up -d

down:
	cd infra && docker compose down -v

lint:
	cd apps/frontend && npm run lint || true
