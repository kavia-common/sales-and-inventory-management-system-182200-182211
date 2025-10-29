from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_billing_address_unicode_and_special_characters():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "UnicodeAddr", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    addr = "Acme GmbH – Straße 1, München, DE • 邮编: 80331 • ✉️: test@example.com"
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-UNICODE-{sale['id']}",
        "billing_address": addr
    })
    assert inv.status_code in (200, 201), inv.text
    assert inv.json()["billing_address"] == addr
