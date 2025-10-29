from datetime import datetime, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_date_equals_sale_date_when_explicit():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale_date = datetime(2024, 5, 20, 14, 15, 0, tzinfo=timezone.utc).isoformat()
    sale_resp = client.post("/sales", json={
        "customer_name": "DateMirror",
        "date": sale_date,
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    inv_num = f"INV-DATE-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()

    assert inv["date"][:19] == sale["date"][:19]
