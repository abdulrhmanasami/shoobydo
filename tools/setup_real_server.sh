#!/bin/bash
# P - Setup real server (Ubuntu 22.04 LTS)

echo "=== P: Setting up real server ==="

# Configuration - UPDATE THESE VALUES
SERVER_IP="YOUR_SERVER_IP"  # Change this to your actual server IP
SSH_USER="ubuntu"           # Change if different

echo "Server IP: $SERVER_IP"
echo "SSH User: $SSH_USER"

# Check if we have a real IP
if [ "$SERVER_IP" = "YOUR_SERVER_IP" ]; then
    echo "❌ Please update SERVER_IP in this script with your actual server IP"
    echo "Then run: ./tools/setup_real_server.sh"
    exit 1
fi

echo "1. Adding SSH public key to server..."
PUB="$(cat ~/.ssh/id_rsa.pub)"
ssh ${SSH_USER}@${SERVER_IP} "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '${PUB}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

echo "2. Configuring firewall..."
ssh ${SSH_USER}@${SERVER_IP} 'sudo ufw allow OpenSSH && sudo ufw allow 80 && sudo ufw allow 443 && sudo ufw --force enable'

echo "3. Installing Docker..."
ssh ${SSH_USER}@${SERVER_IP} 'curl -fsSL https://get.docker.com | sh'

echo "4. Installing Docker Compose..."
ssh ${SSH_USER}@${SERVER_IP} 'sudo mkdir -p /usr/local/lib/docker/cli-plugins && sudo curl -SL https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose && sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose'

echo "5. Starting Docker service..."
ssh ${SSH_USER}@${SERVER_IP} 'sudo systemctl enable docker && sudo systemctl start docker'

echo "6. Testing Docker installation..."
ssh ${SSH_USER}@${SERVER_IP} 'docker --version && docker compose version'

echo "✅ P completed successfully!"
echo "Next: Run S3 to update GitHub secrets"
