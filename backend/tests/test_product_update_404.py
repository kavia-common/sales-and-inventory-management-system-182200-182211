from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_update_nonexistent_product_returns_404():
    resp = client.put("/products/999999", json={"name": "DoesNotExist"})
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Product not found"
