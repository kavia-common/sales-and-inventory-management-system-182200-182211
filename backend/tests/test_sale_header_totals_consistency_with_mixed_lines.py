from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_header_totals_equal_subtotal_plus_gst_with_mixed_lines():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 2:
        return
    p1, p2 = products[0], products[1]
    r = client.post("/sales", json={
        "customer_name": "HeaderTotals",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "unit_price": 3.33, "gst_rate": 9.99},
            {"product_id": p2["id"], "qty": 4}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    subtotal = Decimal(str(sale["subtotal"]))
    gst_total = Decimal(str(sale["gst_total"]))
    grand_total = Decimal(str(sale["grand_total"]))
    assert grand_total == (subtotal + gst_total)
