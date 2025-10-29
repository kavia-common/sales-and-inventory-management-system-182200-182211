from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_after_creation_contains_expected_keys():
    # Create product and sale
    p = client.post("/products", json={
        "name": "ListAfter",
        "sku": "LIST-AFTER-1",
        "price": 4.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    client.post("/sales", json={
        "customer_name": "ListAfterCustomer",
        "line_items": [{"product_id": p["id"], "qty": 1}]
    })
    r = client.get("/sales")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    keys = {"id", "date", "customer_name", "subtotal", "gst_total", "grand_total", "line_items"}
    assert keys.issubset(set(data[0].keys()))
