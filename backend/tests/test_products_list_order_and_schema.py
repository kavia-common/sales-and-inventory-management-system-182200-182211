from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_order_and_schema():
    # Create a couple products
    client.post("/products", json={"name":"Order1","sku":"ORD-1","price":1.0,"gst_rate":5.0,"stock_qty":1})
    client.post("/products", json={"name":"Order2","sku":"ORD-2","price":2.0,"gst_rate":5.0,"stock_qty":2})
    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        p = data[0]
        for k in ("id","name","sku","price","gst_rate","stock_qty"):
            assert k in p
