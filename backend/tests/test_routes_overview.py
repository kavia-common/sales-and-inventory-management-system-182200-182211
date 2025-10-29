from fastapi.testclient import TestClient
from src.api.main import app

def test_routes_overview():
    client = TestClient(app)
    r = client.get("/routes")
    assert r.status_code == 200
    data = r.json()
    assert "health" in data
    assert "products" in data
    assert "/products" in data["products"]
