from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multiple_lines_same_product_inventory_adjustment():
    p = client.post("/products", json={
        "name": "SameProd",
        "sku": "SAME-PROD-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 100
    }).json()
    pid = p["id"]
    start = p["stock_qty"]

    r = client.post("/sales", json={
        "customer_name": "SameLines",
        "line_items": [
            {"product_id": pid, "qty": 2},
            {"product_id": pid, "qty": 3}
        ]
    })
    assert r.status_code in (200, 201), r.text
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["stock_qty"] == start - (2 + 3)
