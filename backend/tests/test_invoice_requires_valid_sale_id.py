from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_requires_valid_sale_id():
    r = client.post("/invoices", json={"sale_id": 9999999, "invoice_number": "INV-NO-SUCH-SALE"})
    assert r.status_code == 404
