from fastapi.testclient import TestClient
from src.api.main import app

def test_inventory_movement_product_not_found():
    client = TestClient(app)
    resp = client.post("/inventory/movements", json={
        "product_id": 999999,
        "change_qty": 1,
        "reason": "Non-existent product"
    })
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Product not found"
