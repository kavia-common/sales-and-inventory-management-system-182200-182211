from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_billing_address_tabs_and_whitespace_preserved():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "TabsAddr", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    addr = "Line1\tTabbed\nLine2\t\tTabbedMore\nEnd"
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-TABS-{sale['id']}",
        "billing_address": addr
    })
    assert inv.status_code in (200, 201), inv.text
    assert inv.json()["billing_address"] == addr
