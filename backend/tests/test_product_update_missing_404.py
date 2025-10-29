from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_missing_returns_404():
    r = client.put("/products/9999999", json={"name": "DoesNotExist"})
    assert r.status_code == 404
