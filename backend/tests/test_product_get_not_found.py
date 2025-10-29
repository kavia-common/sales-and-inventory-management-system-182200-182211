from fastapi.testclient import TestClient
from src.api.main import app

def test_product_get_not_found_404():
    client = TestClient(app)
    resp = client.get("/products/999999")
    assert resp.status_code == 404
    data = resp.json()
    assert data.get("detail") == "Product not found"
