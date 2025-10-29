from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_combined_filters_return_empty_when_no_match():
    client.post("/seed")
    r = client.get("/invoices", params={"invoice_number": "INV-NON-EXIST", "sale_id": 123456789})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) == 0
