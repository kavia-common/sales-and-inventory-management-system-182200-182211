from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_retrieve_by_filters_after_creation():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "FilterAfterCreate", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    invoice_number = f"INV-FLTR-{sale['id']}"
    billing_address = "123 Filter Rd, Unit 5"
    gstin = "29ABCDE1234F1Z6"

    created = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": invoice_number,
        "billing_address": billing_address,
        "gstin": gstin
    })
    assert created.status_code in (200, 201), created.text

    r_by_number = client.get("/invoices", params={"invoice_number": invoice_number})
    assert r_by_number.status_code == 200
    items = r_by_number.json()
    assert any(i.get("invoice_number") == invoice_number for i in items)

    r_by_sale = client.get("/invoices", params={"sale_id": sale["id"]})
    assert r_by_sale.status_code == 200
    items2 = r_by_sale.json()
    assert any(i.get("sale_id") == sale["id"] for i in items2)
