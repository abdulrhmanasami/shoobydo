import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
import os

# Test client
client = TestClient(app)

def test_health_endpoints():
    """Test health endpoints"""
    # Root health
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
    # API health
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_auth_endpoints_structure():
    """Test that auth endpoints are properly structured"""
    # Check if auth router is included
    response = client.get("/docs")
    assert response.status_code == 200
    
    # Check OpenAPI schema for auth endpoints
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    
    # Verify auth paths exist
    auth_paths = [path for path in schema["paths"].keys() if "/auth" in path]
    assert len(auth_paths) > 0, "Auth endpoints not found in OpenAPI schema"

def test_protected_endpoints_require_auth():
    """Test that protected endpoints require authentication"""
    protected_endpoints = [
        "/api/v1/suppliers/",
        "/api/v1/products/", 
        "/api/v1/customers/",
        "/api/v1/orders/",
        "/api/v1/inventory/products/1/stock",
        "/api/v1/reports/kpis"
    ]
    
    for endpoint in protected_endpoints:
        response = client.get(endpoint)
        # Should return 401 or 403 for unauthenticated requests
        assert response.status_code in [401, 403], f"Endpoint {endpoint} should require authentication"

def test_inventory_and_reports_included():
    """Test that inventory and reports routers are properly included"""
    # Check if inventory endpoints exist
    response = client.get("/api/v1/inventory/products/1/stock")
    assert response.status_code in [401, 403], "Inventory endpoint should exist but require auth"
    
    # Check if reports endpoints exist
    response = client.get("/api/v1/reports/kpis")
    assert response.status_code in [401, 403], "Reports endpoint should exist but require auth"

def test_rbac_structure():
    """Test that RBAC is properly implemented"""
    # This test verifies the structure, actual role testing would require a test database
    # Check if require_role dependency is available
    from app.security import require_role
    assert callable(require_role), "require_role function should be available"

def test_jwt_configuration():
    """Test JWT configuration"""
    from app.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
    
    assert SECRET_KEY != "dev-secret-change-me", "SECRET_KEY should be properly configured"
    assert ALGORITHM == "HS256", "JWT algorithm should be HS256"
    assert ACCESS_TOKEN_EXPIRE_MINUTES > 0, "Token expiry should be positive"

def test_cors_configuration():
    """Test CORS configuration"""
    response = client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    
    # CORS should be enabled
    assert "access-control-allow-origin" in response.headers, "CORS headers should be present"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
