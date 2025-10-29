from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_update_price_gst_and_stock_persist():
    # create
    r = client.post("/products", json={
        "name": "NumProd",
        "sku": "NUM-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 3
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # update values
    upd = client.put(f"/products/{pid}", json={
        "price": 12.34,
        "gst_rate": 7.5,
        "stock_qty": 8
    })
    assert upd.status_code == 200, upd.text
    data = upd.json()
    assert Decimal(str(data["price"])) == Decimal("12.34")
    assert Decimal(str(data["gst_rate"])) == Decimal("7.5")
    assert data["stock_qty"] == 8
