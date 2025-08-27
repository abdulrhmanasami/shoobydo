from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def login_admin():
    r = client.post("/auth/login", json={"email":"admin@example.com","password":"admin123"})
    assert r.status_code == 200, r.text
    tok = r.json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}

def test_products_orders_items_crud_flow():
    hdr = login_admin()

    # create product
    import time
    sku = f"SKU{int(time.time())}"
    r = client.post("/products", headers=hdr, json={"sku": sku, "name":"Widget", "price":10.0, "stock":20})
    assert r.status_code in (200,201), r.text
    prod = r.json()
    pid = prod["id"]
    assert prod["stock"] == 20

    # create order
    cmail = f"buyer{int(time.time())}@example.com"
    r = client.post("/orders", headers=hdr, json={"customer_email": cmail, "status":"new", "total":0})
    assert r.status_code in (200,201), r.text
    oid = r.json()["id"]

    # add item qty=3 (stock -> 17, order total -> 30)
    r = client.post(f"/orders/{oid}/items", headers=hdr, json={"product_id": pid, "qty":3, "unit_price":10.0})
    assert r.status_code in (200,201), r.text
    item = r.json()
    iid = item["id"]
    assert item["subtotal"] == 30.0

    # verify list items
    r = client.get(f"/orders/{oid}/items", headers=hdr)
    assert r.status_code == 200
    assert any(x["id"] == iid for x in r.json())

    # update qty -> 5 (stock -> 15, order total -> 50)
    r = client.put(f"/orders/{oid}/items/{iid}", headers=hdr, json={"qty":5})
    assert r.status_code == 200, r.text
    assert r.json()["subtotal"] == 50.0

    # verify order total reflects 50
    r = client.get("/orders", headers=hdr, params={"q":"new"})
    assert r.status_code == 200
    order = next(o for o in r.json() if o["id"] == oid)
    assert float(order["total"]) == 50.0

    # delete item (stock -> 20, order total -> 0)
    r = client.delete(f"/orders/{oid}/items/{iid}", headers=hdr)
    assert r.status_code == 200

    # verify totals & product stock restored
    r = client.get("/orders", headers=hdr, params={"q":"new"})
    order = next(o for o in r.json() if o["id"] == oid)
    assert float(order["total"]) == 0.0

    r = client.get("/products", headers=hdr, params={"q":sku})
    prod = next(p for p in r.json() if p["id"] == pid)
    assert int(prod["stock"]) == 20
