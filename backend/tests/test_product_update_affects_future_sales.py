from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_updating_product_price_and_gst_affects_future_sales_only():
    # Create product
    r = client.post("/products", json={
        "name": "UpdateAffects",
        "sku": "UPD-A-1",
        "price": 100.00,
        "gst_rate": 10.00,
        "stock_qty": 100
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]

    # Create initial sale uses original price/gst
    s1 = client.post("/sales", json={
        "customer_name": "BeforeUpdate",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    # Update product price/gst
    up = client.put(f"/products/{pid}", json={"price": 200.00, "gst_rate": 20.00})
    assert up.status_code == 200, up.text

    # Create second sale should use updated price/gst
    s2 = client.post("/sales", json={
        "customer_name": "AfterUpdate",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    # Validate first sale totals reflect old price/gst
    from decimal import ROUND_HALF_UP
    def q2(x): return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    assert q2(s1["subtotal"]) == q2("100.00")
    assert q2(s1["gst_total"]) == q2("10.00")
    assert q2(s1["grand_total"]) == q2("110.00")

    # Validate second sale totals reflect new price/gst
    assert q2(s2["subtotal"]) == q2("200.00")
    assert q2(s2["gst_total"]) == q2("40.00")
    assert q2(s2["grand_total"]) == q2("240.00")
