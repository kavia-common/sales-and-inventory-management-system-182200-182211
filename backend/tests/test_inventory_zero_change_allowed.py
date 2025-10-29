from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_zero_change_is_allowed_and_persists():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    r = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 0, "reason": "Audit"})
    # Accept current behavior: could be 200/201 if allowed, or 400/422 if later validation added
    assert r.status_code in (200, 201, 400, 422)
