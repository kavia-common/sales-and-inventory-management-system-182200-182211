from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_seed_creates_products_and_list_contains_required_fields():
    r = client.post("/seed")
    assert r.status_code in (200, 201), r.text

    lst = client.get("/products")
    assert lst.status_code == 200
    products = lst.json()
    assert isinstance(products, list)
    assert len(products) >= 1
    required = {"id", "name", "sku", "price", "gst_rate", "stock_qty"}
    assert required.issubset(set(products[0].keys()))
