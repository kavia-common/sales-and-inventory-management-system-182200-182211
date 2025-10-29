from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_missing_invoice_returns_404():
    r = client.get("/invoices/999999")
    assert r.status_code == 404
