from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_filter_by_sale_id():
    # Seed and create a sale
    client.post("/seed")
    sale_resp = client.post("/sales", json={
        "customer_name": "Filter by sale",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    # Create invoice from sale
    invoice_number = f"INV-SALE-{sale_id}"
    inv_resp = client.post("/invoices", json={
        "sale_id": sale_id,
        "invoice_number": invoice_number
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text

    # Filter by sale_id
    list_resp = client.get(f"/invoices?sale_id={sale_id}")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert all(i["sale_id"] == sale_id for i in items)
