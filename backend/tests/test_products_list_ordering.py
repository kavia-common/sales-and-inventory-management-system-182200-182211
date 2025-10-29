from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_returns_descending_id_order():
    # Create at least two products
    a = client.post("/products", json={"name":"A","sku":"ORD-A-1","price":1,"gst_rate":5,"stock_qty":1}).json()
    b = client.post("/products", json={"name":"B","sku":"ORD-B-1","price":1,"gst_rate":5,"stock_qty":1}).json()
    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    # Find consecutive positions for ids
    ids = [p["id"] for p in data]
    assert ids == sorted(ids, reverse=True)
