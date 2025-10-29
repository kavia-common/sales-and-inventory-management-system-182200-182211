from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_large_positive_and_negative_deltas():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial = int(p["stock_qty"])

    # Large add
    add_qty = 100000
    r_add = client.post("/inventory/movements", json={"product_id": pid, "change_qty": add_qty, "reason": "BulkAdd"})
    assert r_add.status_code in (200, 201), r_add.text
    after_add = client.get(f"/products/{pid}").json()["stock_qty"]
    assert int(after_add) == initial + add_qty

    # Large subtract (but not below zero beyond check scope)
    sub_qty = 50000
    r_sub = client.post("/inventory/movements", json={"product_id": pid, "change_qty": -sub_qty, "reason": "BulkRemove"})
    assert r_sub.status_code in (200, 201), r_sub.text
    after_sub = client.get(f"/products/{pid}").json()["stock_qty"]
    assert int(after_sub) == initial + add_qty - sub_qty
