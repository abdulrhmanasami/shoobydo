import os, time, requests, pytest

BASE = f"http://127.0.0.1:{os.getenv('PORT','8800')}"

def _wait():
    for _ in range(10):
        try:
            r = requests.get(f"{BASE}/health", timeout=1)
            if r.ok:
                return True
        except Exception:
            time.sleep(0.5)
    return False

def test_health():
    assert _wait()
    r = requests.get(f"{BASE}/health", timeout=2)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_kpis_and_costs():
    assert _wait()
    r1 = requests.get(f"{BASE}/reports/kpis", timeout=5)
    r2 = requests.get(f"{BASE}/reports/costs", timeout=5)
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert "files" in r1.json()
    assert "total_cost" in r2.json()

def test_upload():
    assert _wait()
    # skip if DB not available
    try:
        ping = requests.get(f"{BASE}/db/ping", timeout=3).json()
        if not ping.get("ok"):
            import pytest; pytest.skip("DB not available for upload test")
    except Exception:
        import pytest; pytest.skip("DB not available for upload test")
    # prepare a tiny xlsx in memory
    import io
    try:
        from openpyxl import Workbook
    except Exception:
        import pytest; pytest.skip("openpyxl missing")
    wb = Workbook()
    ws = wb.active
    ws.append(["col1","col2"]) ; ws.append([1,2])
    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    files = {"file": ("test_upload.xlsx", bio.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = requests.post(f"{BASE}/suppliers/upload", files=files, timeout=10)
    assert r.status_code == 200
    # wrong extension
    files_bad = {"file": ("bad.txt", b"hello", "text/plain")}
    r2 = requests.post(f"{BASE}/suppliers/upload", files=files_bad, timeout=5)
    assert r2.status_code == 400

def test_suppliers_crud():
    assert _wait()
    # Skip if DB is not available
    try:
        ping = requests.get(f"{BASE}/db/ping", timeout=3).json()
        if not ping.get("ok"):
            pytest.skip("DB not available; skipping suppliers CRUD tests")
    except Exception:
        pytest.skip("DB not available; skipping suppliers CRUD tests")
    payload = {"name": "Test Supplier", "file_path": "/tmp/test.xlsx", "rows": 1, "sheets": 1}
    created = requests.post(f"{BASE}/suppliers", json=payload, timeout=5)
    assert created.status_code in (200, 201)
    obj = created.json()
    sid = obj.get("id")
    assert sid
    # get
    got = requests.get(f"{BASE}/suppliers/{sid}", timeout=5)
    assert got.status_code == 200
    # update
    upd = requests.put(f"{BASE}/suppliers/{sid}", json={"name":"Updated"}, timeout=5)
    assert upd.status_code == 200
    assert upd.json().get("name") == "Updated"
    # list
    lst = requests.get(f"{BASE}/suppliers", timeout=5)
    assert lst.status_code == 200
    # delete
    d = requests.delete(f"{BASE}/suppliers/{sid}", timeout=5)
    assert d.status_code == 200


