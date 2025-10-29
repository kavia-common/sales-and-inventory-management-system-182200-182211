from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_name_update_with_unicode_persists():
    r = client.post("/products", json={
        "name": "PlainName",
        "sku": "UNICODE-NAME-1",
        "price": 5.5,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    new_name = "名称 – Ümlaut ✓"
    up = client.put(f"/products/{pid}", json={"name": new_name})
    assert up.status_code == 200, up.text
    assert up.json()["name"] == new_name

    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["name"] == new_name
