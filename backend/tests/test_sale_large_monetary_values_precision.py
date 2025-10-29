from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_large_monetary_values_precision_and_no_overflow():
    # Create product with high price and generous stock
    p = client.post("/products", json={
        "name": "HighValue",
        "sku": "HIGH-VAL-1",
        "price": 99999.99,
        "gst_rate": 28.0,
        "stock_qty": 10000
    }).json()
    qty = 123
    r = client.post("/sales", json={
        "customer_name": "HighValueBuyer",
        "line_items": [{"product_id": p["id"], "qty": qty}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    for key in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(sale[key]))
        assert v == v.quantize(Decimal("0.01"))
