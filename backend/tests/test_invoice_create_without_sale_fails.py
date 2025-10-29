from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_create_without_sale_fails():
    r = client.post("/invoices", json={"invoice_number": "INV-NOSALE-1"})
    assert r.status_code in (400, 404, 422)
