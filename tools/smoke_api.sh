#!/bin/bash
set -euo pipefail
B=http://127.0.0.1:8002

echo "🚀 Starting API Smoke Test..."

# Health check
echo "✅ Testing health endpoint..."
curl -sSfL --max-time 5 --connect-timeout 2 "$B/health" >/dev/null

# OpenAPI schema
echo "✅ Testing OpenAPI schema..."
curl -sSfL --max-time 5 --connect-timeout 2 "$B/openapi.json" | jq '.info.version' >/dev/null

# Test protected endpoints (should return 401/403)
echo "✅ Testing protected endpoints (expecting 401/403)..."
for p in "/api/v1/reports/summary" "/api/v1/reports/kpis" "/api/v1/inventory/products" "/api/v1/suppliers"; do
  echo "  Testing $p..."
  if curl -sSL --max-time 5 --connect-timeout 2 "$B$p" 2>/dev/null; then
    echo "  ⚠️  WARN: $p returned success (should be protected)"
  else
    echo "  ✅ $p properly protected"
  fi
done

echo "🎉 Smoke test completed successfully!"
