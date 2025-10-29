from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_large_values_precision_and_no_overflow():
    # Create product with large price
    p = client.post("/products", json={
        "name": "BigVals",
        "sku": "BIG-VALS-1",
        "price": 999999.99,
        "gst_rate": 18.0,
        "stock_qty": 2000000
    }).json()

    # Create sale with very large qty
    qty = 100000
    r = client.post("/sales", json={
        "customer_name": "BigBuyer",
        "line_items": [{"product_id": p["id"], "qty": qty}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    # Ensure values are parseable and at 2 decimals
    for k in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(sale[k]))
        assert v == v.quantize(Decimal("0.01"))
