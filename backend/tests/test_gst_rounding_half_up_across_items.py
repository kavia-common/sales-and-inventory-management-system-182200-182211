from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_gst_rounding_half_up_across_multiple_items():
    # Create custom products to trigger fractional cents
    p1 = client.post("/products", json={
        "name": "Rounding1",
        "sku": "RND-1",
        "price": 0.99,
        "gst_rate": 5.5,  # 5.5% of 0.99 -> 0.05445
        "stock_qty": 100
    }).json()
    p2 = client.post("/products", json={
        "name": "Rounding2",
        "sku": "RND-2",
        "price": 1.01,
        "gst_rate": 5.5,  # 5.5% of 1.01 -> 0.05555
        "stock_qty": 100
    }).json()

    resp = client.post("/sales", json={
        "customer_name": "Rounding Customer",
        "line_items": [
            {"product_id": p1["id"], "qty": 1},
            {"product_id": p2["id"], "qty": 1},
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Expected rounding half-up per line:
    # Line1 subtotal = 0.99; gst = 0.99 * 0.055 = 0.05445 -> 0.05 (half-up)
    # Line2 subtotal = 1.01; gst = 1.01 * 0.055 = 0.05555 -> 0.06 (half-up)
    # Totals: subtotal=2.00; gst=0.11; grand=2.11
    assert Decimal(str(sale["subtotal"])) == Decimal("2.00")
    assert Decimal(str(sale["gst_total"])) == Decimal("0.11")
    assert Decimal(str(sale["grand_total"])) == Decimal("2.11")
