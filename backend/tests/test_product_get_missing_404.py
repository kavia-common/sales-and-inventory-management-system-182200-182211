from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_get_missing_returns_404():
    r = client.get("/products/99999999")
    assert r.status_code == 404
