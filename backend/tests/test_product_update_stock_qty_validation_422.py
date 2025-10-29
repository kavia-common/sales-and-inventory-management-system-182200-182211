from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_rejects_non_integer_stock_qty():
    # create product
    r = client.post("/products", json={
        "name": "StockVal",
        "sku": "STK-VAL-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 2
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Attempt to update stock_qty with non-integer value
    bad = client.put(f"/products/{pid}", json={"stock_qty": 2.5})
    assert bad.status_code == 422
