from __future__ import annotations
import os
import time
import uuid
from typing import Dict, Tuple
from jose import jwt, JWTError
from .redis_store import get_redis

ACCESS_SECRET = os.getenv("JWT_SECRET_KEY", "changeme-in-dev")
ACCESS_ALG    = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_MIN    = int(os.getenv("JWT_EXPIRES_MINUTES", "30"))

REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET_KEY", "changeme-refresh-dev")
REFRESH_MIN    = int(os.getenv("JWT_REFRESH_EXPIRES_MINUTES", "10080"))  # 7 days


def _now() -> int:
    return int(time.time())


def _exp(minutes: int) -> int:
    return _now() + minutes * 60


def _encode(claims: Dict, secret: str, alg: str = "HS256") -> str:
    return jwt.encode(claims, secret, algorithm=alg)


def _decode(token: str, secret: str) -> Dict:
    return jwt.decode(token, secret, algorithms=[ACCESS_ALG])


def create_access_token(sub: str, role: str) -> Tuple[str, int]:
    exp = _exp(ACCESS_MIN)
    payload = {"sub": sub, "role": role, "type": "access", "jti": str(uuid.uuid4()), "iat": _now(), "exp": exp}
    return _encode(payload, ACCESS_SECRET, ACCESS_ALG), exp


def create_refresh_token(sub: str, role: str) -> Tuple[str, int, str]:
    exp = _exp(REFRESH_MIN)
    jti = str(uuid.uuid4())
    payload = {"sub": sub, "role": role, "type": "refresh", "jti": jti, "iat": _now(), "exp": exp}
    return _encode(payload, REFRESH_SECRET, ACCESS_ALG), exp, jti


def decode_access(token: str) -> Dict:
    return _decode(token, ACCESS_SECRET)


def decode_refresh(token: str) -> Dict:
    return _decode(token, REFRESH_SECRET)


def blacklist_refresh_jti(jti: str, exp_ts: int) -> None:
    r = get_redis()
    if not r:
        return
    ttl = max(0, exp_ts - _now())
    try:
        r.setex(f"jwt:blacklist:{jti}", ttl, "1")
    except Exception:
        pass


def is_refresh_blacklisted(jti: str) -> bool:
    r = get_redis()
    if not r:
        return False
    try:
        return r.exists(f"jwt:blacklist:{jti}") == 1
    except Exception:
        return False


def rotate_refresh(old_refresh: str) -> Tuple[str, int, str]:
    claims = decode_refresh(old_refresh)
    if claims.get("type") != "refresh":
        raise JWTError("invalid token type")
    old_jti = claims.get("jti")
    if old_jti and is_refresh_blacklisted(old_jti):
        raise JWTError("token revoked")
    if old_jti:
        blacklist_refresh_jti(old_jti, claims.get("exp", _now()))
    return create_refresh_token(claims["sub"], claims.get("role", "viewer"))


