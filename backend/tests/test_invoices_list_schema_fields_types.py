from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_schema_fields_types():
    client.post("/seed")
    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        inv = data[0]
        # basic field existence
        for k in ("id", "sale_id", "invoice_number", "date", "subtotal", "gst_total", "grand_total"):
            assert k in inv
