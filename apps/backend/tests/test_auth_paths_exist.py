from app.main import app

def _paths():
    return {r.path for r in app.routes if hasattr(r,"path")}

def test_auth_endpoints_present_canonical_and_alias():
    paths = _paths()
    # canonical
    assert "/api/v1/login" in paths
    assert "/api/v1/register" in paths
    # alias present but قد تكون مخفية عن الـ schema — نتأكد من وجود route
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/register" in paths
