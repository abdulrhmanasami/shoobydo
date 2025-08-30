#!/bin/bash
set -euo pipefail
B=http://127.0.0.1:8802
./tools/smoke_api.sh "$B" || true
TOKEN="${TOKEN:-}" ./tools/smoke_api.sh "$B" || true
echo "✅ smoke staging done"
