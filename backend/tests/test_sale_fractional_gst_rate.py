from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_fractional_gst_rate_calculates_correctly():
    # Create a product with fractional GST rate
    create = client.post("/products", json={
        "name": "FracGST",
        "sku": "FR-GST-075",
        "price": 100.00,
        "gst_rate": 7.5,
        "stock_qty": 10
    })
    assert create.status_code in (200, 201), create.text
    product = create.json()
    pid = product["id"]

    # Create a sale for qty=2, expect subtotal=200.00, gst=15.00, total=215.00
    resp = client.post("/sales", json={
        "customer_name": "Fractional GST",
        "line_items": [{"product_id": pid, "qty": 2}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    assert Decimal(str(sale["subtotal"])) == Decimal("200.00")
    assert Decimal(str(sale["gst_total"])) == Decimal("15.00")
    assert Decimal(str(sale["grand_total"])) == Decimal("215.00")
