from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_partial_update_only_changes_specified_fields():
    # create product
    r = client.post("/products", json={
        "name": "PartialOld",
        "sku": "PART-001",
        "price": 10.00,
        "gst_rate": 5.0,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]

    # partial update: only name
    up = client.put(f"/products/{pid}", json={"name": "PartialNew"})
    assert up.status_code in (200, 201), up.text
    updated = up.json()
    assert updated["name"] == "PartialNew"
    assert updated["sku"] == prod["sku"]
    assert str(updated["price"]) == str(prod["price"])
    assert str(updated["gst_rate"]) == str(prod["gst_rate"])
    assert updated["stock_qty"] == prod["stock_qty"]
