from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_list_after_create():
    # Ensure a product exists
    r = client.post("/products", json={"name":"ListMove","sku":"LM-1","price":2.5,"gst_rate":5.0,"stock_qty":0})
    if r.status_code in (200, 201):
        pid = r.json()["id"]
    else:
        pid = client.get("/products").json()[0]["id"]

    # Create a movement
    r2 = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 5, "reason": "Init stock"})
    assert r2.status_code in (200, 201), r2.text

    # List movements
    r3 = client.get("/inventory/movements")
    assert r3.status_code == 200
    data = r3.json()
    assert isinstance(data, list)
    if data:
        m = data[0]
        for key in ("id", "product_id", "change_qty", "reason", "timestamp"):
            assert key in m
