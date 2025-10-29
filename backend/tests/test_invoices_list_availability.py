from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_endpoint_availability_returns_list():
    r = client.get("/invoices")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
