from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_reason_validation():
    # Create a product to reference
    p = client.post("/products", json={
        "name": "ReasonVal",
        "sku": "RSN-VAL-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 0
    }).json()
    # Send whitespace reason -> should be 422 from pydantic
    r = client.post("/inventory/movements", json={
        "product_id": p["id"],
        "change_qty": 1,
        "reason": "   "
    })
    assert r.status_code == 422, r.text
