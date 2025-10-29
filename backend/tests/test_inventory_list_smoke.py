from fastapi.testclient import TestClient
from src.api.main import app

def test_inventory_list_smoke():
    client = TestClient(app)
    client.post("/seed")
    # create one movement
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "Smoke"})
    resp = client.get("/inventory/movements")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        m = data[0]
        for key in ("id", "product_id", "change_qty", "reason", "timestamp"):
            assert key in m
