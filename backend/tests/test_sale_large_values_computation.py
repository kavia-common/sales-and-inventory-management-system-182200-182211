from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_large_values_computes_totals_correctly():
    # Create product with high price
    r = client.post("/products", json={
        "name": "BigValue",
        "sku": "BIG-VAL-1",
        "price": 999999.99,
        "gst_rate": 18.0,
        "stock_qty": 2000000
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    qty = 123456
    resp = client.post("/sales", json={
        "customer_name": "Big Buyer",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    price = Decimal("999999.99")
    subtotal = (price * qty).quantize(Decimal("0.01"))
    gst = (subtotal * Decimal("18.0") / Decimal("100")).quantize(Decimal("0.01"))
    grand = (subtotal + gst).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == subtotal
    assert Decimal(str(sale["gst_total"])) == gst
    assert Decimal(str(sale["grand_total"])) == grand
