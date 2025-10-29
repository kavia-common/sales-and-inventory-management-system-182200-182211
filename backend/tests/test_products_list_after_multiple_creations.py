from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_after_multiple_creations():
    client.post("/products", json={"name":"Bulk1","sku":"BULK-1","price":1.0,"gst_rate":5.0,"stock_qty":1})
    client.post("/products", json={"name":"Bulk2","sku":"BULK-2","price":2.0,"gst_rate":5.0,"stock_qty":2})
    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for p in data[:2]:
        for k in ("id","name","sku","price","gst_rate","stock_qty"):
            assert k in p
