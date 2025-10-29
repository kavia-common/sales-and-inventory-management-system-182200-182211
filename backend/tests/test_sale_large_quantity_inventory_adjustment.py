from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_large_quantity_inventory_adjustment():
    # Create product with large stock
    p = client.post("/products", json={
        "name": "BulkItem",
        "sku": "BULK-ITEM-1",
        "price": 1.25,
        "gst_rate": 18.0,
        "stock_qty": 200000
    }).json()
    pid = p["id"]
    start_qty = int(p["stock_qty"])

    qty = 12345
    r = client.post("/sales", json={
        "customer_name": "BulkBuyer",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()

    # Inventory decreased
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert int(g.json()["stock_qty"]) == start_qty - qty

    # Totals are numeric and two-decimal safe
    Decimal(str(sale["subtotal"]))
    Decimal(str(sale["gst_total"]))
    Decimal(str(sale["grand_total"]))
