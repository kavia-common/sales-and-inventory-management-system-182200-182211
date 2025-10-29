from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_change_qty_integer_validation():
    # Create a product to reference
    p = client.post("/products", json={
        "name": "QtyType",
        "sku": "QTY-TYPE-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 0
    }).json()

    # Non-integer change_qty should be 422 by schema typing
    r = client.post("/inventory/movements", json={
        "product_id": p["id"],
        "change_qty": 1.5,
        "reason": "Bad qty type"
    })
    assert r.status_code == 422
