from fastapi.testclient import TestClient
from src.api.main import app

def test_openapi_schema_route():
    client = TestClient(app)
    r = client.get("/openapi.json")
    assert r.status_code == 200
    data = r.json()
    assert "openapi" in data
    assert "paths" in data
