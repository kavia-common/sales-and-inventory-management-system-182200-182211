from datetime import datetime, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_preserves_provided_date():
    # Ensure a product exists
    p = client.post("/products", json={
        "name":"DatePreserve",
        "sku":"DATE-PRES-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()
    r = client.post("/sales", json={
        "customer_name": "Backdated",
        "date": dt,
        "line_items": [{"product_id": p["id"], "qty": 1}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert sale["date"].startswith(dt[:19])
