from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_missing_product_returns_404():
    r = client.get("/products/999999")
    assert r.status_code == 404

def test_get_missing_sale_returns_404():
    r = client.get("/sales/999999")
    assert r.status_code == 404
