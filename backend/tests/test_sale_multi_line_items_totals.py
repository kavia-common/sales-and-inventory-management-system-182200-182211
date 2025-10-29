from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_multiple_line_items_calculates_totals_correctly():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]

    resp = client.post("/sales", json={
        "customer_name": "MultiLine",
        "line_items": [
            {"product_id": pid1, "qty": 2},
            {"product_id": pid2, "qty": 3}
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Compute expected totals
    sub1 = (Decimal(str(p1["price"])) * Decimal("2")).quantize(Decimal("0.01"))
    gst1 = (sub1 * Decimal(str(p1["gst_rate"])) / Decimal("100")).quantize(Decimal("0.01"))
    sub2 = (Decimal(str(p2["price"])) * Decimal("3")).quantize(Decimal("0.01"))
    gst2 = (sub2 * Decimal(str(p2["gst_rate"])) / Decimal("100")).quantize(Decimal("0.01"))

    expected_sub = (sub1 + sub2).quantize(Decimal("0.01"))
    expected_gst = (gst1 + gst2).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == expected_sub
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_total
    assert len(sale["line_items"]) == 2
