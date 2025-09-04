#!/bin/bash
# K0 - Setup TLS certificates with Let's Encrypt

echo "=== K0: Setting up TLS certificates ==="

# Configuration - UPDATE THESE VALUES
APP_DOMAIN="app.staging.commisio.dev"
API_DOMAIN="api.staging.commisio.dev"
STATUS_DOMAIN="status.staging.commisio.dev"
EMAIL="your-email@example.com"  # Change this

echo "Domains: $APP_DOMAIN, $API_DOMAIN, $STATUS_DOMAIN"
echo "Email: $EMAIL"

# Check if we have real domains
if [ "$EMAIL" = "your-email@example.com" ]; then
    echo "❌ Please update EMAIL in this script with your actual email"
    echo "Then run: ./tools/setup_tls.sh"
    exit 1
fi

echo "1. Creating certbot directories..."
mkdir -p infra/nginx/certbot/{conf,www}

echo "2. Checking nginx configuration for ACME challenge..."
if grep -q "acme-challenge" infra/nginx/nginx-app.conf; then
    echo "✅ ACME challenge location found in nginx config"
else
    echo "❌ ACME challenge location missing from nginx config"
    echo "Please add to nginx-app.conf:"
    echo "location ^~ /.well-known/acme-challenge/ { root /var/www/certbot; allow all; }"
    exit 1
fi

echo "3. Checking docker-compose volumes..."
if grep -q "certbot" infra/compose/docker-compose.staging.yml; then
    echo "✅ Certbot volumes found in docker-compose"
else
    echo "❌ Certbot volumes missing from docker-compose"
    echo "Please add to nginx service:"
    echo "  volumes:"
    echo "    - ./infra/nginx/certbot/www:/var/www/certbot"
    echo "    - ./infra/nginx/certbot/conf:/etc/letsencrypt"
    exit 1
fi

echo "4. Restarting nginx to serve ACME challenge path..."
docker compose -f infra/compose/docker-compose.staging.yml -f infra/compose/docker-compose.auto.yml up -d nginx

echo "5. Obtaining SSL certificates..."
docker run --rm \
  -v "$(pwd)/infra/nginx/certbot/conf:/etc/letsencrypt" \
  -v "$(pwd)/infra/nginx/certbot/www:/var/www/certbot" \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d "${APP_DOMAIN}" -d "${API_DOMAIN}" -d "${STATUS_DOMAIN}" \
  --agree-tos -m "${EMAIL}" --no-eff-email -n

echo "6. Restarting nginx with SSL certificates..."
docker compose -f infra/compose/docker-compose.staging.yml -f infra/compose/docker-compose.auto.yml restart nginx

echo "✅ K0 completed successfully!"
echo "Next: Run K to test HTTPS endpoints"
