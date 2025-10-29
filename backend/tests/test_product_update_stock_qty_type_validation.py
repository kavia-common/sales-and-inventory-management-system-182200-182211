from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_with_non_integer_stock_qty_rejected():
    r = client.post("/products", json={
        "name": "StockTypeVal",
        "sku": "STK-TYPE-VAL-1",
        "price": 5.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    up = client.put(f"/products/{pid}", json={"stock_qty": 3.14})
    assert up.status_code in (400, 422)
