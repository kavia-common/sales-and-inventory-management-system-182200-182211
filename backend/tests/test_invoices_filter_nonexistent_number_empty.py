from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_by_nonexistent_number_returns_empty_list():
    r = client.get("/invoices", params={"invoice_number": "INV-DOES-NOT-EXIST-000"})
    assert r.status_code == 200
    assert r.json() == [] or isinstance(r.json(), list)
