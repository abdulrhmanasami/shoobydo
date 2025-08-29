import os

# Key rotation support
KEYS = {
    os.getenv("JWT_KID_ACTIVE", "k1"): os.getenv("SECRET_KEY", "shoobydo-dev-secret"),         # الجديدة
    os.getenv("JWT_KID_PREVIOUS", "k0"): os.getenv("SECRET_KEY_OLD", ""), # القديمة (اختياري)
}

ACTIVE_KID = os.getenv("JWT_KID_ACTIVE", "k1")

def get_key_by_kid(kid: str):
    """Get key by kid (key ID)"""
    return KEYS.get(kid, KEYS[ACTIVE_KID])

def get_active_key():
    """Get currently active key"""
    return KEYS[ACTIVE_KID]
