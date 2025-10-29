from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_override_and_default_prices():
    # Create two products
    p1 = client.post("/products", json={"name":"MixPrice1","sku":"MXP-1","price":20.0,"gst_rate":10.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"MixPrice2","sku":"MXP-2","price":15.0,"gst_rate":5.0,"stock_qty":10}).json()

    # Override price only on p2
    r = client.post("/sales", json={
        "customer_name": "MixOverrideDefault",
        "line_items": [
            {"product_id": p1["id"], "qty": 1},                 # subtotal 20.00, gst 2.00
            {"product_id": p2["id"], "qty": 2, "unit_price": 10.0}  # subtotal 20.00, gst 1.00
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert str(Decimal(str(sale["subtotal"]))) == str(Decimal("40.00"))
    assert str(Decimal(str(sale["gst_total"]))) == str(Decimal("3.00"))
    assert str(Decimal(str(sale["grand_total"]))) == str(Decimal("43.00"))
