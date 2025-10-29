from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_denied_when_product_stock_is_zero():
    # Create product with zero stock
    create = client.post("/products", json={
        "name": "ZeroStockSale",
        "sku": "ZS-SALE-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 0
    })
    assert create.status_code in (200, 201), create.text
    pid = create.json()["id"]

    # Attempt sale with qty 1 should fail with 400
    resp = client.post("/sales", json={
        "customer_name": "ZeroStock Buyer",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert resp.status_code == 400
    assert "Insufficient stock" in resp.json().get("detail", "")
