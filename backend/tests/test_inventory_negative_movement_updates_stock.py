from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_negative_inventory_movement_reduces_stock():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial = p["stock_qty"]

    # apply negative movement
    mv = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": -1,
        "reason": "Damage"
    })
    assert mv.status_code in (200, 201), mv.text

    # verify reduced by 1
    updated = client.get(f"/products/{pid}").json()
    assert updated["stock_qty"] == int(initial) - 1
