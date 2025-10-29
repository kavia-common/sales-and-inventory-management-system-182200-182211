from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "OK"

def test_openapi_available():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert "paths" in r.json()
