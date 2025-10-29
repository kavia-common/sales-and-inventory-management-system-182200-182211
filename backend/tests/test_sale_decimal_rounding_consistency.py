from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_decimal_rounding_consistency():
    p = client.post("/products", json={
        "name": "RoundItem",
        "sku": "RND-001",
        "price": 9.995,  # will round to 10.00
        "gst_rate": 12.345,  # will round to 12.35
        "stock_qty": 10
    }).json()
    r = client.post("/sales", json={
        "customer_name": "Round",
        "line_items": [{"product_id": p["id"], "qty": 2}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    # Ensure rounding to 2 decimals
    for k in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(sale[k]))
        assert v == v.quantize(Decimal("0.01"))
    for li in sale["line_items"]:
        for k in ("unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
            v = Decimal(str(li[k]))
            assert v == v.quantize(Decimal("0.01"))
