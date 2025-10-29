from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_not_found_404():
    r = client.get("/invoices/987654321")
    assert r.status_code == 404
