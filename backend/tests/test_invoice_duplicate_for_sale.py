from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_invoice_for_sale_returns_400():
    # Seed products and create sale
    client.post("/seed")
    sale_resp = client.post("/sales", json={
        "customer_name": "Dup Invoice",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    # First invoice create
    inv1 = client.post("/invoices", json={
        "sale_id": sale_id,
        "invoice_number": f"DINV-{sale_id}"
    })
    assert inv1.status_code in (200, 201), inv1.text

    # Second invoice should fail for same sale
    inv2 = client.post("/invoices", json={
        "sale_id": sale_id,
        "invoice_number": f"DINV-{sale_id}-2"
    })
    assert inv2.status_code == 400
