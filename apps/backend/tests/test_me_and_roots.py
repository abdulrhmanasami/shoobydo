import httpx, pytest
from app.main import app

@pytest.mark.anyio
async def test_roots_and_me():
    async with httpx.AsyncClient(app=app, base_url="http://test") as c:
        # جذور الروترات (200/401/403/405 مقبول حسب الحماية)
        for p in ("/api/v1/suppliers","/api/v1/products","/api/v1/customers","/api/v1/orders","/api/v1/inventory","/api/v1/reports"):
            r = await c.get(p if p.endswith("/") else p + "/")
            assert r.status_code in (200,401,403,405)
        # me بدون توكن يجب لا تكون 200
        r = await c.get("/api/v1/me")
        assert r.status_code in (401,403)
