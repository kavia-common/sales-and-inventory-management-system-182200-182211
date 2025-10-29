from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_optional_fields_roundtrip_through_list_and_get():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "Roundtrip", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    addr = "Roundtrip Address, Apt 9B"
    gstin = "07ABCDE1234F1Z1"
    created = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-ROUND-{sale['id']}", "billing_address": addr, "gstin": gstin})
    assert created.status_code in (200, 201), created.text
    inv = created.json()

    # Check via list filter
    lst = client.get("/invoices", params={"invoice_number": inv["invoice_number"]})
    assert lst.status_code == 200
    items = lst.json()
    assert any(i.get("billing_address") == addr and i.get("gstin") == gstin for i in items)

    # Check via get
    got = client.get(f"/invoices/{inv['id']}")
    assert got.status_code == 200
    body = got.json()
    assert body["billing_address"] == addr
    assert body["gstin"] == gstin
