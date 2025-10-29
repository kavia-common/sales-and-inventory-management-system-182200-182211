from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multiple_lines_same_product_aggregate_stock():
    # Create a product with sufficient stock
    p = client.post("/products", json={
        "name": "MultiSame",
        "sku": "MULTI-SAME-1",
        "price": 5.0,
        "gst_rate": 5.0,
        "stock_qty": 20
    }).json()
    pid = p["id"]

    before = client.get(f"/products/{pid}").json()["stock_qty"]

    # Create sale with two lines for the same product
    r = client.post("/sales", json={
        "customer_name": "MultiSameCustomer",
        "line_items": [
            {"product_id": pid, "qty": 3},
            {"product_id": pid, "qty": 4}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert len(sale["line_items"]) == 2

    after = client.get(f"/products/{pid}").json()["stock_qty"]
    assert int(after) == int(before) - (3 + 4)
