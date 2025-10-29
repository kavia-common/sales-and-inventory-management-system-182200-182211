from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_get_includes_line_items_fields():
    # Create product and sale
    p = client.post("/products", json={
        "name": "SaleFields",
        "sku": "SALE-FIELDS-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    s = client.post("/sales", json={
        "customer_name": "Fields",
        "line_items": [{"product_id": p["id"], "qty": 1}]
    }).json()

    r = client.get(f"/sales/{s['id']}")
    assert r.status_code == 200
    sale = r.json()
    assert "line_items" in sale and isinstance(sale["line_items"], list)
    li = sale["line_items"][0]
    for k in ("id", "sale_id", "product_id", "qty", "unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
        assert k in li
