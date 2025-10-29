from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_unknown_product_returns_404():
    r = client.post("/inventory/movements", json={
        "product_id": 999999,
        "change_qty": 1,
        "reason": "NoSuchProduct"
    })
    assert r.status_code == 404
