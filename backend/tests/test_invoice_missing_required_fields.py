from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_missing_required_fields_rejected():
    # Missing both sale_id and invoice_number
    r = client.post("/invoices", json={})
    assert r.status_code in (400, 422), r.text

    # Missing invoice_number
    r2 = client.post("/invoices", json={"sale_id": 1})
    assert r2.status_code in (400, 422), r2.text

    # Missing sale_id
    r3 = client.post("/invoices", json={"invoice_number": "INV-REQ-1"})
    assert r3.status_code in (400, 422), r3.text
