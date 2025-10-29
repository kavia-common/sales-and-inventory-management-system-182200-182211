from fastapi.testclient import TestClient
from src.api.main import app
from datetime import datetime, timezone

client = TestClient(app)

def test_invoice_date_matches_sale():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale_date = datetime(2024, 6, 1, 9, 0, 0, tzinfo=timezone.utc).isoformat()
    sale = client.post("/sales", json={
        "customer_name": "InvoiceDate",
        "date": sale_date,
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-DATE-{sale['id']}"
    }).json()

    # Normalize potential trailing Z
    got = inv["date"].replace("Z", "+00:00")
    assert got.startswith("2024-06-01T09:00:00")
