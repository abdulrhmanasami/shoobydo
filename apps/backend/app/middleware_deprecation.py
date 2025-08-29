from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta, timezone

class DeprecationAlias(BaseHTTPMiddleware):
    """
    Middleware لإضافة ترويسات Deprecation و Sunset لمسارات alias
    """
    async def dispatch(self, req, call_next):
        res = await call_next(req)
        if req.url.path.startswith("/api/v1/auth/"):
            # إزالة في 14 يومًا
            sunset = (datetime.now(timezone.utc) + timedelta(days=14)).strftime("%a, %d %b %Y %H:%M:%S GMT")
            res.headers["Deprecation"] = "true"
            res.headers["Sunset"] = sunset
            res.headers["Warning"] = "299 - 'Deprecated: This endpoint will be removed in v0.9.3'"
        return res
