#!/usr/bin/env bash
set -euo pipefail
scurl() { command curl --max-time 5 --connect-timeout 2 -f -L "$@"; }
# التصدير مدعوم في bash فقط
if [ -n "${BASH_VERSION:-}" ]; then export -f scurl; fi
