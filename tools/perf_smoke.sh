#!/bin/bash
set -euo pipefail
B=${1:-http://127.0.0.1:8801}
P=${2:-/api/v1/reports/summary}
N=${N:-200}
C=${C:-20}
echo "Perf smoke → $B$P  (N=$N, C=$C)"
seq "$N" | xargs -P "$C" -I{} curl -sS -o /dev/null -w "%{http_code}\n" "$B$P" | awk '
{cnt[$1]++} END {for (k in cnt) printf("%s: %d\n", k, cnt[k])}
'
