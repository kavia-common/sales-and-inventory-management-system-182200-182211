from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multiple_lines_same_product_totals_correct():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    price = Decimal(str(p["price"]))
    gst = Decimal(str(p["gst_rate"]))

    # Two separate lines for the same product
    resp = client.post("/sales", json={
        "customer_name": "SameProductLines",
        "line_items": [
            {"product_id": pid, "qty": 1},
            {"product_id": pid, "qty": 2}
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    assert len(sale["line_items"]) == 2

    # Expected totals:
    sub1 = price * 1
    sub2 = price * 2
    subtotal = (sub1 + sub2).quantize(Decimal("0.01"))
    gst_total = ((sub1 * gst / Decimal("100")) + (sub2 * gst / Decimal("100"))).quantize(Decimal("0.01"))
    grand_total = (subtotal + gst_total).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == subtotal
    assert Decimal(str(sale["gst_total"])) == gst_total
    assert Decimal(str(sale["grand_total"])) == grand_total
