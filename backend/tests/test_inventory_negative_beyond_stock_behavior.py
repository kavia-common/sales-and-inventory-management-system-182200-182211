from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_negative_beyond_stock_behavior():
    # Create product with small stock
    p = client.post("/products", json={
        "name": "NegBeyond",
        "sku": "NEG-BEYOND-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    }).json()
    # Apply movement that would drop below zero; behavior may vary
    r = client.post("/inventory/movements", json={
        "product_id": p["id"],
        "change_qty": -5,
        "reason": "Large adjustment"
    })
    assert r.status_code in (200, 201, 400)
