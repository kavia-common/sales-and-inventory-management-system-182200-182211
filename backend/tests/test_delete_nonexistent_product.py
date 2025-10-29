from fastapi.testclient import TestClient
from src.api.main import app

def test_delete_nonexistent_product_404():
    client = TestClient(app)
    resp = client.delete("/products/999999")
    assert resp.status_code == 404
    data = resp.json()
    assert data.get("detail") == "Product not found"
