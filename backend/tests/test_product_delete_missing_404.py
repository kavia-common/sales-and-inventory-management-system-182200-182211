from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_delete_missing_returns_404():
    r = client.delete("/products/9999999")
    assert r.status_code == 404
