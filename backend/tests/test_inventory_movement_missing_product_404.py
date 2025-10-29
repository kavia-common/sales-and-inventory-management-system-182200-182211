from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_for_missing_product_returns_404():
    r = client.post("/inventory/movements", json={
        "product_id": 99999999,
        "change_qty": 1,
        "reason": "MissingProduct"
    })
    assert r.status_code == 404
