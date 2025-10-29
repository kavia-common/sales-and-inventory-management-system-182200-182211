from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_overrides_schema_and_totals():
    # Create two products
    p1 = client.post("/products", json={"name":"MixOv1","sku":"MXO-1","price":10.0,"gst_rate":5.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"MixOv2","sku":"MXO-2","price":20.0,"gst_rate":18.0,"stock_qty":10}).json()

    # Line 1: override gst_rate to 0% (tax exempt)
    # Line 2: override unit_price to 15.50 (with base gst_rate 18%)
    r = client.post("/sales", json={
        "customer_name": "MixedOverrides",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "gst_rate": 0.0},     # subtotal 20.00, gst 0.00
            {"product_id": p2["id"], "qty": 3, "unit_price": 15.50}  # subtotal 46.50, gst 8.37
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()

    # Check presence of keys
    keys = {"id","date","customer_name","subtotal","gst_total","grand_total","line_items"}
    assert keys.issubset(set(sale.keys()))
    assert isinstance(sale["line_items"], list) and len(sale["line_items"]) == 2

    # Totals: subtotal 66.50, gst 8.37, grand 74.87
    assert str(Decimal(str(sale["subtotal"]))) == str(Decimal("66.50"))
    assert str(Decimal(str(sale["gst_total"]))) == str(Decimal("8.37"))
    assert str(Decimal(str(sale["grand_total"]))) == str(Decimal("74.87"))
