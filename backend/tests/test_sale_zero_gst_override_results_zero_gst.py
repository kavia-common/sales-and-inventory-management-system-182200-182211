from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_zero_gst_override_results_in_zero_gst_totals():
    # Create a product with non-zero GST to ensure override actually changes behavior
    r = client.post("/products", json={
        "name": "ZeroGSTOverride",
        "sku": "ZG-OVR-1",
        "price": 50.0,
        "gst_rate": 18.0,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Create sale with gst_rate override = 0
    resp = client.post("/sales", json={
        "customer_name": "ZeroGST Customer",
        "line_items": [{"product_id": pid, "qty": 2, "gst_rate": 0.0}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    assert Decimal(str(sale["subtotal"])) == Decimal("100.00")
    assert Decimal(str(sale["gst_total"])) == Decimal("0.00")
    assert Decimal(str(sale["grand_total"])) == Decimal("100.00")
