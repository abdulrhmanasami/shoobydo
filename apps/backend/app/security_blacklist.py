import os
import time
import redis

# Redis connection
r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

def blacklist(jti: str, ttl: int):
    """
    إضافة JWT إلى القائمة السوداء
    """
    r.setex(f"bl:{jti}", ttl, "1")

def is_blacklisted(jti: str) -> bool:
    """
    فحص إذا كان JWT في القائمة السوداء
    """
    return r.exists(f"bl:{jti}") == 1

def clear_blacklist():
    """
    مسح القائمة السوداء (للتطوير فقط)
    """
    for key in r.scan_iter("bl:*"):
        r.delete(key)
