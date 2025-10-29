from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_create_with_invalid_sale_returns_404():
    resp = client.post("/invoices", json={
        "sale_id": 999999,
        "invoice_number": "INV-NON-EXIST"
    })
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Sale not found"
