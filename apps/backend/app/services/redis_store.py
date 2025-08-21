from __future__ import annotations
import os
from typing import Optional
import redis

_redis: Optional[redis.Redis] = None


def get_redis() -> Optional[redis.Redis]:
    global _redis
    if _redis is not None:
        return _redis
    host = os.getenv("REDIS_HOST", "127.0.0.1")
    port = int(os.getenv("REDIS_PORT", "6379"))
    try:
        _redis = redis.Redis(host=host, port=port, decode_responses=True)
        _redis.ping()
        return _redis
    except Exception:
        return None


