from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_get_missing_returns_404():
    r = client.get("/sales/999999")
    assert r.status_code == 404
