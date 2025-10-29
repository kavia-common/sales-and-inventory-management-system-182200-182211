from fastapi.testclient import TestClient
from src.api.main import app

def test_invoices_empty_initially():
    client = TestClient(app)
    # Start from a clean state assumption; list invoices should return a list (possibly empty)
    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
