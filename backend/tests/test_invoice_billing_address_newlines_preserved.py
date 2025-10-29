from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_billing_address_newlines_preserved_on_get():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "AddrLines", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    addr = "Line1\nLine2\nLine3"
    created = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-LINES-{sale['id']}",
        "billing_address": addr
    })
    assert created.status_code in (200, 201), created.text
    inv = created.json()
    got = client.get(f"/invoices/{inv['id']}")
    assert got.status_code == 200
    assert got.json()["billing_address"] == addr
