from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_duplicate_sku_rejected():
    # Create two products
    p1 = client.post("/products", json={"name":"DupUpdate1","sku":"UPD-DUP-1","price":5.0,"gst_rate":5.0,"stock_qty":1}).json()
    p2 = client.post("/products", json={"name":"DupUpdate2","sku":"UPD-DUP-2","price":6.0,"gst_rate":5.0,"stock_qty":1}).json()
    # Attempt to update p2's SKU to p1's SKU -> should fail with 400
    r = client.put(f"/products/{p2['id']}", json={"sku": p1["sku"]})
    assert r.status_code == 400
