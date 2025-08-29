#!/usr/bin/env bash
set -euo pipefail
cd "${BASH_SOURCE%/*}/.."
files=(-f docker-compose.yml)
[ -f docker-compose.override.yml ] && files+=(-f docker-compose.override.yml)
docker compose "${files[@]}" up -d
