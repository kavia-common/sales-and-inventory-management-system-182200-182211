from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_zero_gst_rate_results_in_zero_tax():
    p = client.post("/products", json={
        "name": "ZeroGST",
        "sku": "ZERO-GST-1",
        "price": 10.0,
        "gst_rate": 0.0,
        "stock_qty": 10
    }).json()
    r = client.post("/sales", json={
        "customer_name": "ZeroGstSale",
        "line_items": [{"product_id": p["id"], "qty": 3, "unit_price": 2.50, "gst_rate": 0.0}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    assert Decimal(str(li["line_gst"])) == Decimal("0.00")
    assert Decimal(str(sale["grand_total"])) == Decimal(str(sale["subtotal"]))
