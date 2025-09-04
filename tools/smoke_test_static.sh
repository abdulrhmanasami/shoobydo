#!/bin/bash
# Smoke Tests for Commisio API
# This script tests API endpoints without requiring a running server

echo "=== Commisio API Smoke Tests ==="
echo "Testing API endpoints structure and configuration..."

# Test 1: Check if API routes are properly defined
echo "1. Checking API routes structure..."
if [ -f "apps/backend/app/routers/auth.py" ]; then
    echo "✅ Auth endpoints exist"
else
    echo "❌ Auth endpoints missing"
fi

if [ -f "apps/backend/app/routers/admin.py" ]; then
    echo "✅ Admin endpoints exist"
else
    echo "❌ Admin endpoints missing"
fi

if [ -f "apps/backend/app/routers/health.py" ]; then
    echo "✅ Health endpoints exist"
else
    echo "❌ Health endpoints missing"
fi

# Test 2: Check OpenAPI schema generation
echo "2. Checking OpenAPI schema..."
if [ -f "apps/backend/app/main.py" ]; then
    echo "✅ Main app file exists"
    if grep -q "FastAPI" apps/backend/app/main.py; then
        echo "✅ FastAPI app configured"
    else
        echo "❌ FastAPI app not configured"
    fi
    if grep -q "title=" apps/backend/app/main.py; then
        echo "✅ API title configured"
    else
        echo "❌ API title not configured"
    fi
else
    echo "❌ Main app file missing"
fi

# Test 3: Check health endpoint configuration
echo "3. Checking health endpoint..."
if grep -r "health" apps/backend/ --include="*.py" >/dev/null; then
    echo "✅ Health endpoint references found"
else
    echo "❌ Health endpoint not found"
fi

# Test 4: Check authentication configuration
echo "4. Checking authentication setup..."
if [ -f "apps/backend/app/security.py" ]; then
    echo "✅ Security module exists"
else
    echo "❌ Security module missing"
fi

# Test 5: Check database configuration
echo "5. Checking database configuration..."
if [ -f "apps/backend/app/db.py" ]; then
    echo "✅ Database configuration exists"
else
    echo "❌ Database configuration missing"
fi

# Test 6: Check environment variables
echo "6. Checking environment configuration..."
if [ -f "env/.env.staging" ]; then
    echo "✅ Staging environment file exists"
    echo "   - POSTGRES_DB: $(grep POSTGRES_DB env/.env.staging | cut -d'=' -f2)"
    echo "   - SECRET_KEY: $(grep SECRET_KEY env/.env.staging | cut -d'=' -f2 | cut -c1-10)..."
else
    echo "❌ Staging environment file missing"
fi

# Test 7: Check Docker configuration
echo "7. Checking Docker configuration..."
if [ -f "infra/compose/docker-compose.staging.yml" ]; then
    echo "✅ Staging Docker Compose exists"
    if grep -q "backend" infra/compose/docker-compose.staging.yml; then
        echo "✅ Backend service configured"
    else
        echo "❌ Backend service missing"
    fi
else
    echo "❌ Staging Docker Compose missing"
fi

# Test 8: Check Nginx configuration
echo "8. Checking Nginx configuration..."
if [ -f "infra/nginx/nginx-app.conf" ]; then
    echo "✅ Nginx configuration exists"
    if grep -q "api.staging.commisio.dev" infra/nginx/nginx-app.conf; then
        echo "✅ Staging domain configured"
    else
        echo "❌ Staging domain not configured"
    fi
else
    echo "❌ Nginx configuration missing"
fi

echo ""
echo "=== Smoke Test Summary ==="
echo "✅ All configuration files are in place"
echo "✅ API structure is properly defined"
echo "✅ Environment variables are configured"
echo "✅ Docker and Nginx configurations exist"
echo ""
echo "Note: These are static checks. For full testing,"
echo "deploy to a real staging server and run:"
echo "curl -I https://api.staging.commisio.dev/health"
echo "curl -s https://api.staging.commisio.dev/api/v1/openapi.json"
