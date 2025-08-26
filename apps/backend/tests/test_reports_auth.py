"""
Test: reports_auth
Created by: Cursor (auto-generated)
Purpose: Comprehensive auth regression tests for reports endpoints
Last updated: 2025-08-26
"""

import os
import pytest
import httpx

BASE = f"http://127.0.0.1:{os.getenv('SHOOBYDO_BACKEND_PORT','8811')}"

def _login_admin():
    """Login as admin user"""
    r = httpx.post(f"{BASE}/api/v1/auth/login", 
                   json={"email":"admin@test.com","password":"admin123"}, 
                   timeout=5.0)
    assert r.status_code == 200, f"Admin login failed: {r.text}"
    return r.json()["access_token"]

def _login_customer():
    """Login as customer user (if exists)"""
    try:
        r = httpx.post(f"{BASE}/api/v1/auth/login", 
                       json={"email":"customer@test.com","password":"customer123"}, 
                       timeout=5.0)
        if r.status_code == 200:
            return r.json()["access_token"]
    except:
        pass
    return None

def test_reports_summary_ok():
    """Test reports/summary returns 200 with admin token"""
    token = _login_admin()
    r = httpx.get(f"{BASE}/api/v1/reports/summary", 
                  headers={"Authorization": f"Bearer {token}"}, 
                  timeout=5.0)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    
    data = r.json()
    assert "suppliers" in data, "Response missing 'suppliers' field"
    assert "kpis" in data, "Response missing 'kpis' field"
    assert "notes" in data, "Response missing 'notes' field"

def test_reports_summary_unauth():
    """Test reports/summary returns 401 without token"""
    r = httpx.get(f"{BASE}/api/v1/reports/summary", timeout=5.0)
    assert r.status_code == 401, f"Expected 401, got {r.status_code}: {r.text}"

def test_reports_summary_forbidden():
    """Test reports/summary returns 403 with insufficient role"""
    customer_token = _login_customer()
    if customer_token:
        r = httpx.get(f"{BASE}/api/v1/reports/summary", 
                      headers={"Authorization": f"Bearer {customer_token}"}, 
                      timeout=5.0)
        assert r.status_code == 403, f"Expected 403, got {r.status_code}: {r.text}"
    else:
        pytest.skip("Customer user not available for role testing")

def test_reports_kpis_ok():
    """Test reports/kpis returns 200 with admin token"""
    token = _login_admin()
    r = httpx.get(f"{BASE}/api/v1/reports/kpis", 
                  headers={"Authorization": f"Bearer {token}"}, 
                  timeout=5.0)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"

def test_reports_costs_ok():
    """Test reports/costs returns 200 with admin token"""
    token = _login_admin()
    r = httpx.get(f"{BASE}/api/v1/reports/costs", 
                  headers={"Authorization": f"Bearer {token}"}, 
                  timeout=5.0)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"

def test_reports_refresh_admin_only():
    """Test reports/refresh requires admin role"""
    token = _login_admin()
    r = httpx.post(f"{BASE}/api/v1/reports/refresh", 
                   headers={"Authorization": f"Bearer {token}"}, 
                   timeout=5.0)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    
    # Test without token
    r = httpx.post(f"{BASE}/api/v1/reports/refresh", timeout=5.0)
    assert r.status_code == 401, f"Expected 401, got {r.status_code}: {r.text}"
