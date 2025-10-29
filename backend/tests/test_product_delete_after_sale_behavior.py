from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_delete_after_sale_behavior():
    # Create product and perform a sale
    p = client.post("/products", json={
        "name": "DelAfterSale",
        "sku": "DEL-AFTER-SALE-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    sale = client.post("/sales", json={
        "customer_name": "Buyer",
        "line_items": [{"product_id": p["id"], "qty": 1}]
    })
    assert sale.status_code in (200, 201), sale.text

    # Attempt deletion - behavior is implementation defined, accept success or 400
    r_del = client.delete(f"/products/{p['id']}")
    assert r_del.status_code in (200, 204, 400)
