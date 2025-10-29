from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_totals_match_sale():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale_resp = client.post("/sales", json={
        "customer_name": "Totals Match",
        "line_items": [{"product_id": pid, "qty": 2}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    inv_resp = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": f"INV-MATCH-{sale['id']}"
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text
    invoice = inv_resp.json()

    for key in ("subtotal", "gst_total", "grand_total"):
        assert Decimal(str(invoice[key])) == Decimal(str(sale[key]))
