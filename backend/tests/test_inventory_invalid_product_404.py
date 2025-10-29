from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_invalid_product_returns_404():
    resp = client.post("/inventory/movements", json={
        "product_id": 999999,
        "change_qty": 1,
        "reason": "Invalid"
    })
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Product not found"
