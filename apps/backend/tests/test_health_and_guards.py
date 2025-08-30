from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)

def test_health_ok():
    r = c.get("/health")
    assert r.status_code in (200, 204)
def test_reports_guarded():
    for p in ["/api/v1/reports/summary", "/api/v1/reports/kpis"]:
        r = c.get(p)
        assert r.status_code in (401,403,404)
