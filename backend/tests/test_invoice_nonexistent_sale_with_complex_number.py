from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_nonexistent_sale_with_complex_number_rejected():
    complex_no = "INV-🚀-2025_02_29-#" + ("Z" * 50)
    r = client.post("/invoices", json={"sale_id": 987654321, "invoice_number": complex_no})
    assert r.status_code in (404, 422)
