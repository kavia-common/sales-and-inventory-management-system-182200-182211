from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_optional_fields_persistence():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "OptFields", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-OPT-{sale['id']}"
    payload = {
        "sale_id": sale["id"],
        "invoice_number": inv_no,
        "billing_address": "221B Baker Street, London",
        "gstin": "22AAAAA0000A1Z5"
    }
    r = client.post("/invoices", json=payload)
    assert r.status_code in (200, 201), r.text
    inv = r.json()
    assert inv["billing_address"] == payload["billing_address"]
    assert inv["gstin"] == payload["gstin"]
