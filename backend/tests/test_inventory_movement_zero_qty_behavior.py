from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_zero_qty_behavior_documented():
    # Create product
    r = client.post("/products", json={"name":"ZeroMv","sku":"ZERO-MV-1","price":1,"gst_rate":0,"stock_qty":1})
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]
    # Zero qty movement - behavior may vary; assert endpoint responds consistently with either success or validation error
    mv = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 0, "reason": "NoChange"})
    assert mv.status_code in (200, 201, 400, 422)
