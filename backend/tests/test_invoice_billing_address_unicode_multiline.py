from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_billing_address_unicode_and_multiline_persists():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "UnicodeAddr", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    addr = "ACME Corp.\nAttn: José Álvarez\n42 Rue de l'Université\nParis, Île-de-France 75007 🇫🇷"
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-ADDR-{sale['id']}",
        "billing_address": addr
    })
    assert inv.status_code in (200, 201), inv.text
    data = inv.json()
    assert data["billing_address"] == addr
