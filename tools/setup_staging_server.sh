#!/bin/bash
# S1 - Setup SSH on real server + update GitHub secrets

echo "=== S1: Setting up SSH on real server ==="

# Configuration - UPDATE THESE VALUES
SERVER_IP="YOUR_SERVER_IP"  # Change this to your actual server IP
SSH_USER="ubuntu"           # Change if different

echo "Server IP: $SERVER_IP"
echo "SSH User: $SSH_USER"

# Check if we have a real IP
if [ "$SERVER_IP" = "YOUR_SERVER_IP" ]; then
    echo "❌ Please update SERVER_IP in this script with your actual server IP"
    echo "Then run: ./tools/setup_staging_server.sh"
    exit 1
fi

echo "1. Adding public key to server..."
PUB="$(cat ~/.ssh/id_rsa.pub)"
ssh ${SSH_USER}@${SERVER_IP} "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '${PUB}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

echo "2. Testing SSH connection..."
ssh -i ~/.ssh/id_rsa ${SSH_USER}@${SERVER_IP} 'echo "SSH connection successful" && uname -a'

echo "3. Updating GitHub secrets..."
gh secret set STAGING_HOST --body "$SERVER_IP"
gh secret set STAGING_USER --body "$SSH_USER"
gh secret set STAGING_SSH_PRIVATE_KEY < ~/.ssh/id_rsa

echo "4. Updating environment secret..."
base64 -w0 env/.env.staging 2>/dev/null || base64 env/.env.staging | tr -d '\n' > /tmp/staging.env.b64
gh secret set STAGING_ENV_B64 < /tmp/staging.env.b64

echo "✅ S1 completed successfully!"
echo "Next: Run S2 to deploy to staging server"
