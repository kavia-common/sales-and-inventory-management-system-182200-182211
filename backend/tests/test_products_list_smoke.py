from fastapi.testclient import TestClient
from src.api.main import app

def test_products_list_smoke():
    client = TestClient(app)
    client.post("/seed")
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        p = data[0]
        for key in ("id", "name", "sku", "price", "gst_rate", "stock_qty"):
            assert key in p
