from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_gst_overrides_totals():
    # Create two products with different base GST
    p1 = client.post("/products", json={
        "name": "MixGST-1",
        "sku": "MIX-GST-1",
        "price": 50.0,
        "gst_rate": 18.0,
        "stock_qty": 10
    }).json()
    p2 = client.post("/products", json={
        "name": "MixGST-2",
        "sku": "MIX-GST-2",
        "price": 30.0,
        "gst_rate": 12.0,
        "stock_qty": 10
    }).json()

    # Override GST on second item to 5%
    r = client.post("/sales", json={
        "customer_name": "MixedGST",
        "line_items": [
            {"product_id": p1["id"], "qty": 1},                 # 50 @ 18% => gst 9.00
            {"product_id": p2["id"], "qty": 2, "gst_rate": 5.0} # 60 @ 5% => gst 3.00
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert str(sale["subtotal"]) == str(Decimal("110.00"))
    assert str(sale["gst_total"]) == str(Decimal("12.00"))
    assert str(sale["grand_total"]) == str(Decimal("122.00"))
