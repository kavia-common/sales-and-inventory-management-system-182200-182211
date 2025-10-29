from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_allows_zero_unit_price_override_and_computes_totals():
    # Create product
    p = client.post("/products", json={
        "name": "ZeroPrice",
        "sku": "ZERO-PRICE-1",
        "price": 5.0,
        "gst_rate": 10.0,
        "stock_qty": 5
    }).json()

    r = client.post("/sales", json={
        "customer_name": "FreeItem",
        "line_items": [{"product_id": p["id"], "qty": 2, "unit_price": 0.0}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    assert Decimal(str(li["unit_price"])) == Decimal("0.00")
    assert Decimal(str(sale["grand_total"])) == Decimal(str(sale["gst_total"])) + Decimal(str(sale["subtotal"]))
    assert Decimal(str(sale["subtotal"])) == Decimal("0.00")
