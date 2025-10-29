from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_updates_product_stock():
    # Create product
    r = client.post("/products", json={
        "name": "AdjStock",
        "sku": "ADJ-001",
        "price": 1.00,
        "gst_rate": 0.0,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]
    initial = prod["stock_qty"]

    # Add 3 units
    mv = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": 3,
        "reason": "Restock"
    })
    assert mv.status_code in (200, 201), mv.text
    # Verify
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["stock_qty"] == initial + 3
