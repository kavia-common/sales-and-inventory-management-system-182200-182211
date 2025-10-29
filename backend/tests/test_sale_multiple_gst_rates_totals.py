from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_multiple_gst_rates_computes_totals_correctly():
    # Create two products with different GST rates
    p1 = client.post("/products", json={
        "name": "GST-A",
        "sku": "GST-A-001",
        "price": 100.00,
        "gst_rate": 5.00,
        "stock_qty": 50
    }).json()
    p2 = client.post("/products", json={
        "name": "GST-B",
        "sku": "GST-B-001",
        "price": 200.00,
        "gst_rate": 18.00,
        "stock_qty": 50
    }).json()

    resp = client.post("/sales", json={
        "customer_name": "MultiGST",
        "line_items": [
            {"product_id": p1["id"], "qty": 2},
            {"product_id": p2["id"], "qty": 1}
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Expected calculations
    sub1 = Decimal("100.00") * Decimal("2")  # 200.00
    gst1 = (sub1 * Decimal("5.00") / Decimal("100")).quantize(Decimal("0.01"))
    sub2 = Decimal("200.00") * Decimal("1")  # 200.00
    gst2 = (sub2 * Decimal("18.00") / Decimal("100")).quantize(Decimal("0.01"))

    expected_sub = (sub1 + sub2).quantize(Decimal("0.01"))
    expected_gst = (gst1 + gst2).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    from decimal import Decimal as D
    assert D(str(sale["subtotal"])) == expected_sub
    assert D(str(sale["gst_total"])) == expected_gst
    assert D(str(sale["grand_total"])) == expected_total
