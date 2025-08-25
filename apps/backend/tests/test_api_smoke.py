import os, httpx, json

BASE = f"http://127.0.0.1:{os.getenv("SHOOBYDO_BACKEND_PORT","8811")}"

def _login():
    r = httpx.post(f"{BASE}/api/v1/auth/login", json={"email":"admin@example.com","password":"admin123"}, timeout=5.0)
    assert r.status_code==200, r.text
    return r.json()["access_token"]

def test_health():
    r = httpx.get(f"{BASE}/health", timeout=5.0)
    assert r.status_code==200

def test_suppliers_list():
    token = _login()
    r = httpx.get(f"{BASE}/api/v1/suppliers", headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
    assert r.status_code==200
    assert isinstance(r.json(), list)

def test_reports_summary():
    token = _login()
    r = httpx.get(f"{BASE}/api/v1/reports/summary", headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
    assert r.status_code==200, r.text
    assert isinstance(r.json(), dict)
