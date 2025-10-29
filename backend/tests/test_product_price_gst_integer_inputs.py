from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_product_integer_price_and_gst_are_accepted_and_serialized():
    r = client.post("/products", json={
        "name": "IntFields",
        "sku": "INT-100",
        "price": 100,       # integer input
        "gst_rate": 18,     # integer input
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    data = r.json()
    # Ensure JSON numbers are parseable as decimals
    assert Decimal(str(data["price"])) == Decimal("100")
    assert Decimal(str(data["gst_rate"])) == Decimal("18")
