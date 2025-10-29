from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_duplicate_number_400():
    # Seed and create sale
    client.post("/seed")
    sale_resp = client.post("/sales", json={
        "customer_name": "Dup Invoice Number",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    number = f"DUP-NUM-{sale_id}"

    # Create first invoice
    inv1 = client.post("/invoices", json={"sale_id": sale_id, "invoice_number": number})
    assert inv1.status_code in (200, 201), inv1.text

    # Attempt create another invoice with same number but different sale (create another sale)
    sale2_resp = client.post("/sales", json={
        "customer_name": "Another Sale",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale2_resp.status_code in (200, 201), sale2_resp.text
    sale2_id = sale2_resp.json()["id"]

    inv2 = client.post("/invoices", json={"sale_id": sale2_id, "invoice_number": number})
    assert inv2.status_code == 400
