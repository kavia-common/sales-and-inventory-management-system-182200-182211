from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_list_schema_integrity_multiple_entries():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create a couple of movements
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "AddOne"})
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": -1, "reason": "RemoveOne"})

    r = client.get("/inventory/movements")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        keys = set(data[0].keys())
        expected = {"id", "product_id", "change_qty", "reason", "timestamp"}
        assert expected.issubset(keys)
