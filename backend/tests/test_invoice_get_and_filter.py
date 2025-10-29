from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_and_filter():
    # Seed and create a sale
    client.post("/seed")
    sale_resp = client.post("/sales", json={
        "customer_name": "Filter Invoice",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    # Create invoice from sale
    invoice_number = f"INV-FLTR-{sale_id}"
    inv_resp = client.post("/invoices", json={
        "sale_id": sale_id,
        "invoice_number": invoice_number
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()
    inv_id = inv["id"]

    # Get by ID
    get_resp = client.get(f"/invoices/{inv_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["invoice_number"] == invoice_number

    # Filter by invoice_number
    list_resp = client.get(f"/invoices?invoice_number={invoice_number}")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert any(i["invoice_number"] == invoice_number for i in items)
