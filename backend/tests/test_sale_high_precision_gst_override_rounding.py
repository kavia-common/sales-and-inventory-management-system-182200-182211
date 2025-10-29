from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_high_precision_gst_override_rounding():
    p = client.post("/products", json={
        "name": "HiPrecGST",
        "sku": "HP-GST-1",
        "price": 19.99,
        "gst_rate": 18.0,
        "stock_qty": 10
    }).json()

    r = client.post("/sales", json={
        "customer_name": "HPGST",
        "line_items": [{"product_id": p["id"], "qty": 2, "gst_rate": 12.3456}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    # Subtotal = 39.98; GST at 12.35% (rounded) => 4.94; grand 44.92
    assert str(Decimal(str(sale["subtotal"]))) == str(Decimal("39.98"))
    assert str(Decimal(str(sale["gst_total"]))) == str(Decimal("4.94"))
    assert str(Decimal(str(sale["grand_total"]))) == str(Decimal("44.92"))
