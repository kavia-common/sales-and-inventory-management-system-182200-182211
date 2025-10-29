from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_idempotent_no_changes():
    r = client.post("/products", json={
        "name": "Idempotent",
        "sku": "IDEMP-1",
        "price": 3.21,
        "gst_rate": 5.0,
        "stock_qty": 7
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]

    up = client.put(f"/products/{pid}", json={})
    assert up.status_code in (200, 201), up.text
    updated = up.json()
    assert updated["id"] == pid
    assert updated["name"] == prod["name"]
    assert updated["sku"] == prod["sku"]
    assert str(updated["price"]) == str(prod["price"])
    assert str(updated["gst_rate"]) == str(prod["gst_rate"])
    assert updated["stock_qty"] == prod["stock_qty"]
