from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_requires_existing_sale():
    resp = client.post("/invoices", json={"sale_id": 0, "invoice_number": "INV-REQ-0"})
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Sale not found"
