from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_price_and_gst_round_to_two_decimals_on_update():
    r = client.post("/products", json={
        "name": "PrecisionProd",
        "sku": "PREC-PROD-1",
        "price": 0.0,
        "gst_rate": 0.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    up = client.put(f"/products/{pid}", json={"price": 12.3456, "gst_rate": 18.999})
    assert up.status_code in (200, 201), up.text
    p = up.json()

    # Ensure these can be parsed to two decimals
    assert Decimal(str(p["price"])) == Decimal(str(p["price"])).quantize(Decimal("0.01"))
    assert Decimal(str(p["gst_rate"])) == Decimal(str(p["gst_rate"])).quantize(Decimal("0.01"))
