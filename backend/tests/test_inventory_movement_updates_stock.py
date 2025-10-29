from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_updates_stock_up_and_down():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial = int(p["stock_qty"])

    # Add 5 units
    r_add = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 5, "reason": "Restock"})
    assert r_add.status_code in (200, 201), r_add.text
    after_add = client.get(f"/products/{pid}").json()["stock_qty"]
    assert int(after_add) == initial + 5

    # Remove 2 units
    r_sub = client.post("/inventory/movements", json={"product_id": pid, "change_qty": -2, "reason": "Damage"})
    assert r_sub.status_code in (200, 201), r_sub.text
    after_sub = client.get(f"/products/{pid}").json()["stock_qty"]
    assert int(after_sub) == initial + 3
