from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_quantity_must_be_integer_rejected_decimal():
    p = client.post("/products", json={
        "name": "IntQtyOnly",
        "sku": "INT-QTY-ONLY-1",
        "price": 2.0,
        "gst_rate": 5.0,
        "stock_qty": 10
    }).json()
    r = client.post("/sales", json={
        "customer_name": "BadQty",
        "line_items": [{"product_id": p["id"], "qty": 1.5}]
    })
    assert r.status_code in (400, 422)
