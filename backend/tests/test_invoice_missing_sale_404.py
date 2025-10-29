from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_for_missing_sale_returns_404():
    resp = client.post("/invoices", json={"sale_id": 99999999, "invoice_number": "INV-MISS-001"})
    assert resp.status_code == 404
    assert "Sale not found" in resp.json().get("detail", "")
