#!/bin/bash
# L - Clean up old dry-run workflows

echo "=== L: Cleaning up old workflows ==="

echo "1. Checking for old dry-run workflows..."
if [ -f ".github/workflows/deploy-staging.yml" ]; then
    echo "Found old dry-run workflow, removing..."
    git rm .github/workflows/deploy-staging.yml
    git commit -m "ci: remove dry-run workflow to avoid confusion"
    git push
    echo "✅ Old workflow removed"
else
    echo "No old workflows found"
fi

echo "2. Listing current workflows..."
gh workflow list

echo "✅ L completed successfully!"
echo "All workflows cleaned up!"
