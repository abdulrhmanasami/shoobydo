#!/bin/bash
# S2 - Deploy to staging server via workflow

echo "=== S2: Deploying to staging server ==="

echo "1. Running staging deployment workflow..."
gh workflow run cd-staging.yml --ref develop

echo "2. Watching deployment progress..."
echo "Press Ctrl+C to stop watching (deployment will continue in background)"
gh run watch --exit-status

echo "✅ S2 completed!"
echo "Next: Run K0 to setup TLS certificates"
