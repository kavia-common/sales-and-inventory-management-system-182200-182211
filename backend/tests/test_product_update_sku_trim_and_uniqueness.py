from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_sku_trim_and_uniqueness():
    p1 = client.post("/products", json={"name":"TrimUniq1","sku":"TU-1","price":1.0,"gst_rate":5.0,"stock_qty":1}).json()
    p2 = client.post("/products", json={"name":"TrimUniq2","sku":"TU-2","price":1.0,"gst_rate":5.0,"stock_qty":1}).json()

    # Attempt to set p2's sku to p1's sku with whitespace around it
    r = client.put(f"/products/{p2['id']}", json={"sku": f"  {p1['sku']}  "})
    assert r.status_code == 400
