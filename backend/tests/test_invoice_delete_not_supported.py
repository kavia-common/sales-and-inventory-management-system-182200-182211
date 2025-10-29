from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_delete_not_supported_returns_404_or_405():
    # There is no delete endpoint for invoices; ensure calling it fails gracefully
    resp = client.delete("/invoices/1")
    assert resp.status_code in (404, 405)
