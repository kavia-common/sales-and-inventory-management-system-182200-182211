from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_product_price_rounding_to_two_decimals():
    # Create product
    r = client.post("/products", json={
        "name": "Rounder",
        "sku": "ROUND-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Update price with more than two decimals
    upd = client.put(f"/products/{pid}", json={"price": 12.34567})
    assert upd.status_code == 200, upd.text
    data = upd.json()
    # Ensure price is serialized with two decimal places
    assert Decimal(str(data["price"])) == Decimal("12.35")
