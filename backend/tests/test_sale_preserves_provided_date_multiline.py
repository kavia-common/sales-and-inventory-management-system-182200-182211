from datetime import datetime, timezone
from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_preserves_provided_date_multiline():
    # Create two products
    p1 = client.post("/products", json={"name":"DateP1","sku":"DATE-P1","price":5.0,"gst_rate":5.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"DateP2","sku":"DATE-P2","price":7.0,"gst_rate":12.0,"stock_qty":10}).json()
    dt = datetime(2022, 6, 30, 8, 30, 0, tzinfo=timezone.utc).isoformat()
    r = client.post("/sales", json={
        "customer_name": "BackdatedMulti",
        "date": dt,
        "line_items": [
            {"product_id": p1["id"], "qty": 2},
            {"product_id": p2["id"], "qty": 1}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert sale["date"].startswith(dt[:19])
    # Sanity check totals parseable
    for k in ("subtotal","gst_total","grand_total"):
        Decimal(str(sale[k]))
