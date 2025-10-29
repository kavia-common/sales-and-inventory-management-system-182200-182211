from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_list():
    # Ensure seed and at least one movement exist
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "Test movement"})
    resp = client.get("/inventory/movements")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
