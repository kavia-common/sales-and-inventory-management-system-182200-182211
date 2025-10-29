from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_duplicate_number_and_per_sale_constraints():
    client.post("/seed")
    # Create sale
    products = client.get("/products").json()
    pid = products[0]["id"]
    sale_resp = client.post("/sales", json={
        "customer_name": "Dup Invoice",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    # Create first invoice
    inv_num = "INV-DUP-001"
    first = client.post("/invoices", json={"sale_id": sale_id, "invoice_number": inv_num})
    assert first.status_code in (200, 201), first.text

    # Duplicate number on a different sale
    sale2_resp = client.post("/sales", json={
        "customer_name": "Dup Invoice 2",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    sale2_id = sale2_resp.json()["id"]
    dup_num = client.post("/invoices", json={"sale_id": sale2_id, "invoice_number": inv_num})
    assert dup_num.status_code == 400

    # Duplicate invoice for same sale
    dup_sale = client.post("/invoices", json={"sale_id": sale_id, "invoice_number": "INV-DUP-002"})
    assert dup_sale.status_code == 400
