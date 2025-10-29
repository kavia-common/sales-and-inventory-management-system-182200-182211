from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_totals_and_stock_decrement():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial_stock = int(p["stock_qty"])

    qty = 2
    sale_resp = client.post("/sales", json={
        "customer_name": "Totals Tester",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    # Verify totals consistency: subtotal + gst_total = grand_total
    subtotal = Decimal(str(sale["subtotal"]))
    gst_total = Decimal(str(sale["gst_total"]))
    grand_total = Decimal(str(sale["grand_total"]))
    assert subtotal + gst_total == grand_total

    # Verify stock decremented
    updated = client.get(f"/products/{pid}").json()
    assert int(updated["stock_qty"]) == initial_stock - qty
