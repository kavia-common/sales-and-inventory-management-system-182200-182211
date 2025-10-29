from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_includes_created_sale():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    created = client.post("/sales", json={
        "customer_name": "Listed Sale",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert created.status_code in (200, 201), created.text
    sale_id = created.json()["id"]

    lst = client.get("/sales")
    assert lst.status_code == 200
    data = lst.json()
    assert any(s["id"] == sale_id for s in data)
    for s in data:
        for key in ("id", "customer_name", "subtotal", "gst_total", "grand_total"):
            assert key in s
