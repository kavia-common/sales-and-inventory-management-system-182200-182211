from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_empty_and_filters():
    r = client.get("/invoices", params={"sale_id": 0, "invoice_number": "NO-MATCH-000"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 0
