#!/bin/bash
# S3 - Update GitHub secrets with real values

echo "=== S3: Updating GitHub secrets ==="

# Configuration - UPDATE THESE VALUES
SERVER_IP="YOUR_SERVER_IP"  # Change this to your actual server IP
SSH_USER="ubuntu"           # Change if different

echo "Server IP: $SERVER_IP"
echo "SSH User: $SSH_USER"

# Check if we have a real IP
if [ "$SERVER_IP" = "YOUR_SERVER_IP" ]; then
    echo "❌ Please update SERVER_IP in this script with your actual server IP"
    echo "Then run: ./tools/update_github_secrets.sh"
    exit 1
fi

echo "1. Updating STAGING_HOST..."
gh secret set STAGING_HOST --body "$SERVER_IP"

echo "2. Updating STAGING_USER..."
gh secret set STAGING_USER --body "$SSH_USER"

echo "3. Updating STAGING_SSH_PRIVATE_KEY..."
gh secret set STAGING_SSH_PRIVATE_KEY < ~/.ssh/id_rsa

echo "4. Updating STAGING_ENV_B64..."
cat env/.env.staging | base64 | tr -d '\n' > /tmp/staging.env.b64
gh secret set STAGING_ENV_B64 < /tmp/staging.env.b64

echo "5. Testing SSH connection..."
ssh ${SSH_USER}@${SERVER_IP} 'echo ok'

echo "✅ S3 completed successfully!"
echo "Next: Run J3 to deploy to real server"
