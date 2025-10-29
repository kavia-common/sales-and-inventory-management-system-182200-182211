from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_negative_movement_removes_stock():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    before = products[0]["stock_qty"]

    # Remove 2 units
    resp = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": -2,
        "reason": "Shrinkage"
    })
    assert resp.status_code in (200, 201), resp.text

    after = client.get(f"/products/{pid}").json()["stock_qty"]
    assert after == before - 2
