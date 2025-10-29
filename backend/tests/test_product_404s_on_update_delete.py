from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_update_missing_product_returns_404():
    r = client.put("/products/987654321", json={"name": "Nope"})
    assert r.status_code == 404

def test_delete_missing_product_returns_404():
    r = client.delete("/products/987654321")
    assert r.status_code == 404
