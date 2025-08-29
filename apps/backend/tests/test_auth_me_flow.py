import httpx, pytest, jwt
from app.main import app

@pytest.mark.anyio
async def test_login_and_me_200():
    async with httpx.AsyncClient(app=app, base_url="http://test") as c:
        r = await c.post("/api/v1/login", json={"email":"admin@example.com","password":"P@ssw0rd!"})
        assert r.status_code == 200, r.text
        token = r.json()["access_token"]
        # /me => 200
        r = await c.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200, r.text
        # تحقق أن sub نصي (متوافق مع jose)
        payload = jwt.decode(token, options={"verify_signature": False})
        assert isinstance(payload["sub"], str)
