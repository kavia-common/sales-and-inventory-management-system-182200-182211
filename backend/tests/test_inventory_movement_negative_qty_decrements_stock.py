from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_negative_qty_decrements_stock():
    # Create product with known stock
    r = client.post("/products", json={
        "name": "NegMove",
        "sku": "NEG-MOVE-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 10
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]
    start_qty = prod["stock_qty"]

    # Create negative movement
    mv = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": -3,
        "reason": "Adjustment"
    })
    assert mv.status_code in (200, 201), mv.text
    body = mv.json()
    assert body["product_id"] == pid
    assert body["change_qty"] == -3

    # Verify product stock decremented
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["stock_qty"] == start_qty - 3
