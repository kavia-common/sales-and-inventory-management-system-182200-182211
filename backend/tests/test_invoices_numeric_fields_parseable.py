from decimal import Decimal, InvalidOperation
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_numeric_fields_are_parseable_decimals():
    client.post("/seed")
    products = client.get("/products").json()
    if products:
        pid = products[0]["id"]
        s = client.post("/sales", json={"customer_name": "NumParse", "line_items": [{"product_id": pid, "qty": 1}]})
        if s.status_code in (200, 201):
            sale = s.json()
            client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-NUMPARSE-{sale['id']}"})
    r = client.get("/invoices")
    assert r.status_code == 200
    for inv in r.json():
        for k in ("subtotal", "gst_total", "grand_total"):
            try:
                Decimal(str(inv[k]))
            except (InvalidOperation, KeyError):
                assert False, f"Field {k} not parseable as Decimal"
