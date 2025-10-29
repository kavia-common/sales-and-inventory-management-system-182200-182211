from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_for_missing_sale_404_and_filter_empty():
    resp = client.post("/invoices", json={"sale_id": 123456789, "invoice_number": "INV-NO-SALE-1"})
    assert resp.status_code == 404

    # Ensure filtering with that invoice number yields empty list
    lst = client.get("/invoices", params={"invoice_number": "INV-NO-SALE-1"})
    assert lst.status_code == 200
    assert isinstance(lst.json(), list)
    assert len(lst.json()) == 0
