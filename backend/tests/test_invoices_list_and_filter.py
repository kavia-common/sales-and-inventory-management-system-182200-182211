from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_and_filter_by_number():
    client.post("/seed")
    # Create a sale and invoice
    products = client.get("/products").json()
    pid = products[0]["id"]
    sale = client.post("/sales", json={
        "customer_name": "Invoice Filter",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()
    inv_num = f"INV-FLT-{sale['id']}"
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": inv_num
    })
    assert inv.status_code in (200, 201), inv.text

    # List all
    all_resp = client.get("/invoices")
    assert all_resp.status_code == 200
    all_invoices = all_resp.json()
    assert isinstance(all_invoices, list)
    assert any(i["invoice_number"] == inv_num for i in all_invoices)

    # Filter by number
    flt = client.get(f"/invoices?invoice_number={inv_num}")
    assert flt.status_code == 200
    items = flt.json()
    assert any(i["invoice_number"] == inv_num for i in items)
