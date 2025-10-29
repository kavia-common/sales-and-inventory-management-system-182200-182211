from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_update_gst_fractional_and_sale_uses_new_rate():
    # Create product
    r = client.post("/products", json={
        "name": "GSTFrac",
        "sku": "GST-F-1",
        "price": 50.00,
        "gst_rate": 5.0,
        "stock_qty": 10
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Update GST rate to fractional 7.5
    upd = client.put(f"/products/{pid}", json={"gst_rate": 7.5})
    assert upd.status_code == 200, upd.text
    assert Decimal(str(upd.json()["gst_rate"])) == Decimal("7.5")

    # Create a sale and ensure new GST is used
    s = client.post("/sales", json={
        "customer_name": "GSTFracCust",
        "line_items": [{"product_id": pid, "qty": 2}]
    })
    assert s.status_code in (200, 201), s.text
    sale = s.json()
    assert Decimal(str(sale["subtotal"])) == Decimal("100.00")
    # 7.5% of 100.00 = 7.50
    assert Decimal(str(sale["gst_total"])) == Decimal("7.50")
    assert Decimal(str(sale["grand_total"])) == Decimal("107.50")
