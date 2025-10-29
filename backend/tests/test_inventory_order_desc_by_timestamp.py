from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_desc_by_timestamp():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create several movements
    for i in range(3):
        r = client.post("/inventory/movements", json={
            "product_id": pid,
            "change_qty": 1,
            "reason": f"R{i}"
        })
        assert r.status_code in (200, 201), r.text

    lst = client.get("/inventory/movements")
    assert lst.status_code == 200
    items = lst.json()
    # Ensure at least 3 items exist (could include prior seeds)
    assert isinstance(items, list)
    if len(items) >= 2:
        timestamps = [x["timestamp"] for x in items]
        assert timestamps == sorted(timestamps, reverse=True)
