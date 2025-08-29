#!/usr/bin/env bash
set -euo pipefail
echo "docker" > .backend_mode   # default: docker; options: docker|local
echo "[mode] backend -> docker"
