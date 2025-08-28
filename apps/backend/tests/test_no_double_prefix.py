from fastapi.routing import APIRoute
from app.main import app

def test_no_double_segment_prefix():
    dupes=[]
    for r in app.routes:
        if isinstance(r, APIRoute):
            p=r.path
            for seg in ("auth","products","customers","orders","suppliers","inventory","reports"):
                if f"/{seg}/{seg}" in p:
                    dupes.append(p)
    assert not dupes, f"Duplicate segment prefixes: {dupes}"
