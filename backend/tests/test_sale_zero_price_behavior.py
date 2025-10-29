from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_zero_unit_price_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    resp = client.post("/sales", json={
        "customer_name": "ZeroPrice",
        "line_items": [{"product_id": pid, "qty": 1, "unit_price": 0.0}]
    })
    # Accept either validation rejection or acceptance with zero totals
    assert resp.status_code in (200, 201, 400, 422), resp.text
    if resp.status_code in (200, 201):
        sale = resp.json()
        assert Decimal(str(sale["subtotal"])) == Decimal("0.00")
        assert Decimal(str(sale["grand_total"])) == Decimal("0.00")
