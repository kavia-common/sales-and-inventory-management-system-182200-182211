from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_delete_nonexistent_product_404():
    resp = client.delete("/products/999999")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Product not found"
