from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_contains_items_and_totals():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create a sale to ensure at least one record exists
    resp = client.post("/sales", json={
        "customer_name": "ListTester",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert resp.status_code in (200, 201), resp.text

    lst = client.get("/sales")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    if data:
        sale = data[0]
        for key in ("id", "date", "customer_name", "subtotal", "gst_total", "grand_total", "line_items"):
            assert key in sale
        assert isinstance(sale["line_items"], list)
        if sale["line_items"]:
            li = sale["line_items"][0]
            for lkey in ("id", "sale_id", "product_id", "qty", "unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
                assert lkey in li
