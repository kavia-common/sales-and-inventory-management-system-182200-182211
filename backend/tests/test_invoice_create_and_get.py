from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_create_and_get_by_id():
    # Ensure seed data exists
    client.post("/seed")

    # Create a sale first
    products = client.get("/products").json()
    assert products, "Seed should have created products"
    pid = products[0]["id"]
    sale_resp = client.post("/sales", json={
        "customer_name": "Invoice Customer",
        "line_items": [
            {"product_id": pid, "qty": 2}
        ]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()
    sale_id = sale["id"]

    # Create an invoice from the sale
    inv_num = f"INV-{sale_id}"
    inv_resp = client.post("/invoices", json={
        "sale_id": sale_id,
        "invoice_number": inv_num,
        "billing_address": "123 Test St, City",
        "gstin": "22AAAAA0000A1Z5"
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text
    invoice = inv_resp.json()
    assert invoice["sale_id"] == sale_id
    assert invoice["invoice_number"] == inv_num

    # Get invoice by ID
    got = client.get(f"/invoices/{invoice['id']}")
    assert got.status_code == 200
    assert got.json()["invoice_number"] == inv_num
