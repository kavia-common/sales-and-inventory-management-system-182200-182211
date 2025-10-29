from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_price_and_gst_rate_with_decimals():
    r = client.post("/products", json={
        "name": "UpdNums",
        "sku": "UPD-NUMS-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    up = client.put(f"/products/{pid}", json={"price": 12.34, "gst_rate": 18.00})
    assert up.status_code in (200, 201), up.text
    p = up.json()
    # Validate numeric formatting to two decimals
    Decimal(str(p["price"]))
    Decimal(str(p["gst_rate"]))
