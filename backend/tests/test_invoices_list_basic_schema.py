from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_basic_schema_fields():
    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        inv = data[0]
        for key in ("id", "sale_id", "invoice_number", "subtotal", "gst_total", "grand_total"):
            assert key in inv
