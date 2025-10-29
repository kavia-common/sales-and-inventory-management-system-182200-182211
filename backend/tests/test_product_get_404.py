from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_product_404():
    resp = client.get("/products/999999")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Product not found"
