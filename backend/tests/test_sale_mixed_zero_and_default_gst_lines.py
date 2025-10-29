from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_zero_and_default_gst_lines():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]
    price1, price2 = Decimal(str(p1["price"])), Decimal(str(p2["price"]))
    default_gst2 = Decimal(str(p2["gst_rate"]))

    qty1, qty2 = 2, 3

    # Override GST to zero for first line, use default for second
    resp = client.post("/sales", json={
        "customer_name": "MixedZeroGST",
        "line_items": [
            {"product_id": pid1, "qty": qty1, "gst_rate": 0.0},
            {"product_id": pid2, "qty": qty2}
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    sub1 = (price1 * qty1).quantize(Decimal("0.01"))
    gst1 = Decimal("0.00")
    sub2 = (price2 * qty2).quantize(Decimal("0.01"))
    gst2 = (sub2 * default_gst2 / Decimal("100")).quantize(Decimal("0.01"))

    expected_sub = (sub1 + sub2).quantize(Decimal("0.01"))
    expected_gst = (gst1 + gst2).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == expected_sub
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_total
