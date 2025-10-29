from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_single_qty_price_matches_subtotal_and_tax():
    p = client.post("/products", json={
        "name": "SingleQty",
        "sku": "SINGLE-QTY-1",
        "price": 9.99,
        "gst_rate": 18.0,
        "stock_qty": 5
    }).json()
    unit_price = Decimal("3.40")
    r = client.post("/sales", json={
        "customer_name": "SingleQty",
        "line_items": [{"product_id": p["id"], "qty": 1, "unit_price": float(unit_price)}]
    })
    assert r.status_code in (200, 201), r.text
    li = r.json()["line_items"][0]
    assert Decimal(str(li["line_subtotal"])) == unit_price
    # GST should be product's 18% by default
    expected_gst = (unit_price * Decimal("0.18")).quantize(Decimal("0.01"))
    assert Decimal(str(li["line_gst"])) == expected_gst
