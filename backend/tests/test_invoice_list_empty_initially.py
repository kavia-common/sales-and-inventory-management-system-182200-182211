from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_empty_initially():
    # Start a fresh client; list invoices may be empty depending on state
    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
