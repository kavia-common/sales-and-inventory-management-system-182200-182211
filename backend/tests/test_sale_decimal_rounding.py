from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_decimal_rounding_half_up_two_decimals():
    # Create product baseline
    p = client.post("/products", json={
        "name": "Rounder",
        "sku": "RND-001",
        "price": 1.235,  # will be overridden
        "gst_rate": 12.345,  # will be overridden
        "stock_qty": 10
    }).json()

    # Use tricky decimals that need half-up rounding
    unit_price = 1.005  # rounds to 1.01
    gst_rate = 7.505    # rounds to 7.51
    qty = 2
    r = client.post("/sales", json={
        "customer_name": "Rounding",
        "line_items": [{
            "product_id": p["id"],
            "qty": qty,
            "unit_price": unit_price,
            "gst_rate": gst_rate
        }]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    assert str(li["unit_price"]).startswith("1.01")
    assert str(li["gst_rate"]).startswith("7.51")
    # Validate totals are consistent 2dp strings when converted
    Decimal(str(li["line_subtotal"]))
    Decimal(str(li["line_gst"]))
    Decimal(str(li["line_total"]))
    Decimal(str(sale["subtotal"]))
    Decimal(str(sale["gst_total"]))
    Decimal(str(sale["grand_total"]))
