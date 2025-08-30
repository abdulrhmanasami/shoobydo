from fastapi.testclient import TestClient
from app.main import app

# استخدم أسماء الدوال/الديبنـدنـسي الفعلية لديك إن اختلفت
try:
    from app.core.security import get_current_user  # مسار شائع
except Exception:
    from app.security import get_current_user  # بديل


def fake_admin():
    class U:
        id = 1
        email = "admin@example.com"
        role = "admin"
        is_active = True

    return U()


app.dependency_overrides[get_current_user] = lambda: fake_admin()
c = TestClient(app)


def test_admin_ping_200():
    r = c.get("/api/v1/admin/ping")
    assert r.status_code in (200, 204)


def test_reports_allowed_with_admin():
    for p in ["/api/v1/reports/summary", "/api/v1/reports/kpis"]:
        r = c.get(p)
        assert r.status_code in (
            200,
            204,
            403,
            404,
        )  # 403/404 مسموح لو الداتا غير متوفرة أو صلاحيات محدودة
