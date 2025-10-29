from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_by_number_returns_404_when_not_found_initially():
    r = client.get("/invoices/by-number/INV-NOT-FOUND-000")
    assert r.status_code == 404
