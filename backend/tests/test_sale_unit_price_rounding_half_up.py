from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_unit_price_rounds_half_up_to_two_decimals():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Use a unit price with more than 2 decimals to test rounding behavior
    unit_price = 12.3456
    qty = 3

    resp = client.post("/sales", json={
        "customer_name": "RoundingTest",
        "line_items": [{"product_id": pid, "qty": qty, "unit_price": unit_price}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = sale["line_items"][0]

    # Expect rounded unit price 12.35 with HALF_UP
    assert Decimal(str(li["unit_price"])) == Decimal("12.35")
    expected_sub = Decimal("12.35") * Decimal(qty)
    expected_sub = expected_sub.quantize(Decimal("0.01"))
    assert Decimal(str(li["line_subtotal"])) == expected_sub
