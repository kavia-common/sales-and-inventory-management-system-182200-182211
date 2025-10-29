from datetime import datetime, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_date_equals_sale_date_when_provided():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    dt = datetime(2024, 12, 31, 23, 59, 0, tzinfo=timezone.utc).isoformat()
    sale = client.post("/sales", json={
        "customer_name": "MirrorDate",
        "date": dt,
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()
    inv = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-DATE-MIRROR-{sale['id']}"
    })
    assert inv.status_code in (200, 201), inv.text
    assert inv.json()["date"].startswith(dt[:19])
