from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_list_descending_order():
    # Ensure at least two movements with different timestamps
    p = client.post("/products", json={"name":"OrderTS","sku":"ORD-TS-1","price":1.0,"gst_rate":5.0,"stock_qty":0}).json()
    client.post("/inventory/movements", json={"product_id": p["id"], "change_qty": 1, "reason": "M1"})
    client.post("/inventory/movements", json={"product_id": p["id"], "change_qty": 1, "reason": "M2"})
    r = client.get("/inventory/movements")
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    if len(items) >= 2:
        assert items[0]["timestamp"] >= items[1]["timestamp"]
