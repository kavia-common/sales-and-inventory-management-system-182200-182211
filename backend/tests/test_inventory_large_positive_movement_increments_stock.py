from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_large_positive_movement_increments_stock():
    # Create product with initial stock 0
    p = client.post("/products", json={
        "name": "BigRestock",
        "sku": "RST-BIG-1",
        "price": 3.0,
        "gst_rate": 5.0,
        "stock_qty": 0
    }).json()
    pid = p["id"]

    # Apply large positive movement
    qty = 1000
    r = client.post("/inventory/movements", json={"product_id": pid, "change_qty": qty, "reason": "Big Restock"})
    assert r.status_code in (200, 201), r.text

    # Verify stock increased
    p2 = client.get(f"/products/{pid}").json()
    assert int(p2["stock_qty"]) == qty

    # Movement exists
    moves = client.get("/inventory/movements").json()
    assert any(m["product_id"] == pid and int(m["change_qty"]) == qty for m in moves)
