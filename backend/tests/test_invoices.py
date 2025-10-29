from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_flow():
    # Seed some products (idempotent)
    client.post("/seed")

    # Create a sale for product 1 (assumes seed created product id 1)
    sale_resp = client.post("/sales", json={
        "customer_name": "Invoice Tester",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()
    sale_id = sale["id"]

    # Create invoice from sale
    inv_resp = client.post("/invoices", json={
        "sale_id": sale_id,
        "invoice_number": f"INV-AUTO-{sale_id}"
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()
    assert inv["sale_id"] == sale_id

    # List invoices
    list_resp = client.get("/invoices")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(i["sale_id"] == sale_id for i in items)
