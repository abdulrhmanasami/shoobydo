import httpx, pytest, jwt
from app.main import app
try:
    from app.config import settings
    SECRET = settings.SECRET_KEY
    ALG = getattr(settings, "JWT_ALGORITHM", "HS256")
except Exception:
    import os
    SECRET = os.getenv("SECRET_KEY", "shoobydo-dev-secret")
    ALG = os.getenv("JWT_ALGORITHM", "HS256")

@pytest.mark.anyio
async def test_login_and_me_200():
    async with httpx.AsyncClient(app=app, base_url="http://test") as c:
        r = await c.post("/api/v1/login", json={"email":"admin@example.com","password":"P@ssw0rd!"})
        assert r.status_code == 200, r.text
        token = r.json()["access_token"]
        # sub نصي (توافق jose)
        payload = jwt.decode(token, SECRET, algorithms=[ALG])
        assert isinstance(payload["sub"], str)
        # /me 200
        r = await c.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200, r.text
