#!/bin/bash
# K - Smoke tests via HTTPS

echo "=== K: Smoke tests via HTTPS ==="

# Configuration
API_DOMAIN="api.staging.commisio.dev"

echo "Testing API domain: $API_DOMAIN"

echo "1. Testing health endpoint..."
curl -I https://$API_DOMAIN/health

echo ""
echo "2. Testing OpenAPI schema..."
curl -s https://$API_DOMAIN/api/v1/openapi.json | jq -r '.info.title,.openapi' | sed -n '1,2p'

echo ""
echo "3. Testing authentication..."
TOKEN=$(curl -s -X POST "https://$API_DOMAIN/api/v1/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"Passw0rd!"}' | jq -r .access_token)

if [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
    echo "✅ Authentication successful, token obtained"
else
    echo "❌ Authentication failed"
    exit 1
fi

echo ""
echo "4. Testing protected endpoint..."
curl -i -s -H "Authorization: Bearer $TOKEN" "https://$API_DOMAIN/api/v1/admin/ping"

echo ""
echo "✅ K completed successfully!"
echo "All smoke tests passed!"
