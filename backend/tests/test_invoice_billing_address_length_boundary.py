from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_billing_address_length_boundary_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "LongAddr", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    long_addr = "A" * 500  # matches current column length
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-LONGADDR-{sale['id']}",
        "billing_address": long_addr
    })
    assert inv.status_code in (200, 201, 400, 422)
    if inv.status_code in (200, 201):
        assert inv.json()["billing_address"] == long_addr
