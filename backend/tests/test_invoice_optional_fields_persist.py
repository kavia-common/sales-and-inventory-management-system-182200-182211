from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_optional_fields_persist():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "Optional Fields",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    inv_num = f"INV-OPT-{sale['id']}"
    addr = "221B Baker Street"
    gstin = "22AAAAA0000A1Z5"
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": inv_num,
        "billing_address": addr,
        "gstin": gstin
    })
    assert inv.status_code in (200, 201), inv.text
    data = inv.json()
    assert data["billing_address"] == addr
    assert data["gstin"] == gstin
