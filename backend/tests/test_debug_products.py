from fastapi.testclient import TestClient
from src.api.main import app

def test_debug_products_endpoint():
    client = TestClient(app)
    client.post("/seed")
    r = client.get("/debug/products")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert "sku" in data[0]
        assert "stock_qty" in data[0]
