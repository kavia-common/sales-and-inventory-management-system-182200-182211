from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_create_for_missing_sale_404():
    r = client.post("/invoices", json={"sale_id": 999999, "invoice_number": "INV-MISS-999"})
    assert r.status_code == 404
