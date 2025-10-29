from fastapi.testclient import TestClient
from src.api.main import app

def test_invoice_not_found_404():
    client = TestClient(app)
    resp = client.get("/invoices/999999")
    assert resp.status_code == 404
    data = resp.json()
    assert data.get("detail") == "Invoice not found"
