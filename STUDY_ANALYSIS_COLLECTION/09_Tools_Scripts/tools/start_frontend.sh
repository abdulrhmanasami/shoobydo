#!/usr/bin/env bash
set -euo pipefail
. .env.dev
cd apps/frontend
pm="npm"; [ -f pnpm-lock.yaml ] && pm="pnpm"; [ -f yarn.lock ] && pm="yarn"
if [ ! -d node_modules ]; then
  case "$pm" in
    pnpm) command -v pnpm >/dev/null 2>&1 || npm i -g pnpm >/dev/null; pnpm i >/dev/null ;;
    yarn) command -v yarn  >/dev/null 2>&1 || npm i -g yarn  >/dev/null;  yarn   >/dev/null ;;
    npm)  npm i >/dev/null ;;
  esac
fi
lsof -ti :"${FRONTEND_PORT:-3000}" | xargs -r kill -9
case "$pm" in
  pnpm) nohup pnpm dev -- -p "${FRONTEND_PORT:-3000}"  > "/tmp/next.${FRONTEND_PORT:-3000}.log" 2>&1 & echo $! > "/tmp/next.${FRONTEND_PORT:-3000}.pid" ;;
  yarn) nohup yarn dev -p "${FRONTEND_PORT:-3000}"     > "/tmp/next.${FRONTEND_PORT:-3000}.log" 2>&1 & echo $! > "/tmp/next.${FRONTEND_PORT:-3000}.pid" ;;
  npm)  nohup npm run dev -- -p "${FRONTEND_PORT:-3000}" > "/tmp/next.${FRONTEND_PORT:-3000}.log" 2>&1 & echo $! > "/tmp/next.${FRONTEND_PORT:-3000}.pid" ;;
 esac
sleep 2; tail -n 8 "/tmp/next.${FRONTEND_PORT:-3000}.log" || true
echo "[ok] frontend on http://127.0.0.1:${FRONTEND_PORT:-3000}"
