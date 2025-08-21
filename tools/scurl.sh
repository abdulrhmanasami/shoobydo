#!/usr/bin/env bash
set -euo pipefail
scurl() { curl --max-time 5 --connect-timeout 2 -f -L "$@"; }
export -f scurl
