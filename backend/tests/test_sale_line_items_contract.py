from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_items_include_required_fields():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    resp = client.post("/sales", json={
        "customer_name": "LineItemsContract",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    assert "line_items" in sale and isinstance(sale["line_items"], list)
    li = sale["line_items"][0]
    for key in ("id", "sale_id", "product_id", "qty", "unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
        assert key in li
