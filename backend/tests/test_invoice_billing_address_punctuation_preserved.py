from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_billing_address_punctuation_preserved():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "PunctAddr", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    addr = "ACME Corp., 123 Main St.; Suite #500; City, State 12345"
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-PUNCT-{sale['id']}",
        "billing_address": addr
    })
    assert inv.status_code in (200, 201), inv.text
    assert inv.json()["billing_address"] == addr
