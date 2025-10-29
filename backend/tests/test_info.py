from fastapi.testclient import TestClient
from src.api.main import app

def test_info_endpoint():
    client = TestClient(app)
    r = client.get("/info")
    assert r.status_code == 200
    data = r.json()
    assert data.get("name") == "Sales & Inventory Management API"
    assert "db_port" in data
    assert "db_name" in data
