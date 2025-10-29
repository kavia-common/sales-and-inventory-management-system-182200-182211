from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_negative_movement_decrements_stock():
    # Create product with stock
    p = client.post("/products", json={
        "name": "NegMove",
        "sku": "NEG-MV-1",
        "price": 2.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    pid = p["id"]

    # Apply negative movement
    r = client.post("/inventory/movements", json={"product_id": pid, "change_qty": -2, "reason": "Adjustment"})
    assert r.status_code in (200, 201), r.text

    # Verify stock decreased
    p2 = client.get(f"/products/{pid}").json()
    assert int(p2["stock_qty"]) == 3

    # Verify movement appears in list
    moves = client.get("/inventory/movements").json()
    assert any(m["product_id"] == pid and int(m["change_qty"]) == -2 for m in moves)
