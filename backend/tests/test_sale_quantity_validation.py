from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_rejects_zero_or_negative_qty():
    # Create product
    p = client.post("/products", json={
        "name": "QtyVal",
        "sku": "QTY-VAL-1",
        "price": 2.5,
        "gst_rate": 5.0,
        "stock_qty": 10
    }).json()
    # Zero qty
    s0 = client.post("/sales", json={"customer_name": "Zero", "line_items": [{"product_id": p["id"], "qty": 0}]})
    assert s0.status_code in (400, 422)
    # Negative qty
    sn = client.post("/sales", json={"customer_name": "Neg", "line_items": [{"product_id": p["id"], "qty": -1}]})
    assert sn.status_code in (400, 422)
