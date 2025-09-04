#!/bin/bash
# K0 - Setup TLS certificates (Let's Encrypt)

echo "=== K0: Setting up TLS certificates ==="

# Configuration - UPDATE THESE VALUES
SERVER_IP="YOUR_SERVER_IP"  # Change this to your actual server IP
SSH_USER="ubuntu"           # Change if different
APP_DOMAIN="app.staging.commisio.dev"
API_DOMAIN="api.staging.commisio.dev"
STATUS_DOMAIN="status.staging.commisio.dev"
EMAIL="your-email@example.com"  # Change this

echo "Server IP: $SERVER_IP"
echo "Domains: $APP_DOMAIN, $API_DOMAIN, $STATUS_DOMAIN"
echo "Email: $EMAIL"

# Check if we have real values
if [ "$SERVER_IP" = "YOUR_SERVER_IP" ] || [ "$EMAIL" = "your-email@example.com" ]; then
    echo "❌ Please update SERVER_IP and EMAIL in this script"
    echo "Then run: ./tools/setup_tls_real.sh"
    exit 1
fi

echo "1. Creating certbot directories..."
mkdir -p infra/nginx/certbot/{conf,www}

echo "2. Starting nginx to serve ACME challenge..."
ssh ${SSH_USER}@${SERVER_IP} 'cd ~/commisio-deploy && docker compose -f infra/compose/docker-compose.staging.yml -f infra/compose/docker-compose.auto.yml up -d nginx'

echo "3. Obtaining SSL certificates..."
ssh ${SSH_USER}@${SERVER_IP} "\
  docker run --rm \
  -v ~/commisio-deploy/infra/nginx/certbot/conf:/etc/letsencrypt \
  -v ~/commisio-deploy/infra/nginx/certbot/www:/var/www/certbot \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d ${APP_DOMAIN} -d ${API_DOMAIN} -d ${STATUS_DOMAIN} \
  --agree-tos -m ${EMAIL} --no-eff-email -n"

echo "4. Restarting nginx with SSL certificates..."
ssh ${SSH_USER}@${SERVER_IP} 'cd ~/commisio-deploy && docker compose -f infra/compose/docker-compose.staging.yml -f infra/compose/docker-compose.auto.yml restart nginx'

echo "5. Verifying certificates..."
ssh ${SSH_USER}@${SERVER_IP} 'docker exec $(docker ps -q --filter name=nginx) ls -la /etc/letsencrypt/live/'

echo "✅ K0 completed successfully!"
echo "Next: Run K to test HTTPS endpoints"
