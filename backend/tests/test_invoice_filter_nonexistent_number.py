from fastapi.testclient import TestClient
from src.api.main import app

def test_invoice_filter_nonexistent_number_returns_empty_list():
    client = TestClient(app)
    resp = client.get("/invoices?invoice_number=INV-DOES-NOT-EXIST-999")
    assert resp.status_code == 200
    assert resp.json() == []
