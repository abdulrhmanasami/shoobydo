#!/bin/bash
# J3 - Deploy to real server via workflow

echo "=== J3: Deploying to real server ==="

# Configuration - UPDATE THESE VALUES
SERVER_IP="YOUR_SERVER_IP"  # Change this to your actual server IP
SSH_USER="ubuntu"           # Change if different

echo "Server IP: $SERVER_IP"
echo "SSH User: $SSH_USER"

# Check if we have a real IP
if [ "$SERVER_IP" = "YOUR_SERVER_IP" ]; then
    echo "❌ Please update SERVER_IP in this script with your actual server IP"
    echo "Then run: ./tools/deploy_real.sh"
    exit 1
fi

echo "1. Running real deployment workflow..."
gh workflow run cd-staging.yml --ref develop

echo "2. Watching deployment progress..."
echo "Press Ctrl+C to stop watching (deployment will continue in background)"
gh run watch --exit-status

echo "3. Checking deployment status on server..."
ssh ${SSH_USER}@${SERVER_IP} 'cd ~/commisio-deploy && docker compose -f infra/compose/docker-compose.staging.yml -f infra/compose/docker-compose.auto.yml ps'

echo "✅ J3 completed successfully!"
echo "Next: Run K0 to setup TLS certificates"
