from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_missing_sale_id_returns_422():
    resp = client.post("/invoices", json={"invoice_number": "INV-MISS-SALEID-1"})
    assert resp.status_code in (400, 422)
