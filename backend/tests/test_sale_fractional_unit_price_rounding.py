from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_fractional_unit_price_rounding():
    p = client.post("/products", json={
        "name": "FracPrice",
        "sku": "FRAC-PR-1",
        "price": 1.0,
        "gst_rate": 10.0,
        "stock_qty": 10
    }).json()

    # Use fractional unit_price that needs rounding
    r = client.post("/sales", json={
        "customer_name": "Frac",
        "line_items": [{"product_id": p["id"], "qty": 3, "unit_price": 2.333}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    # Subtotal = 3 * 2.333 -> 3 * 2.33 = 6.99 after rounding, GST 10% -> 0.70, total 7.69
    assert str(sale["subtotal"]) == str(Decimal("6.99"))
    assert str(sale["gst_total"]) == str(Decimal("0.70"))
    assert str(sale["grand_total"]) == str(Decimal("7.69"))
