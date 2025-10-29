from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_entries_include_customer_and_totals():
    client.post("/seed")
    products = client.get("/products").json()
    if products:
        pid = products[0]["id"]
        client.post("/sales", json={"customer_name": "FieldsCheck", "line_items": [{"product_id": pid, "qty": 1}]})
    r = client.get("/sales")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        s = data[0]
        assert "customer_name" in s
        for k in ("subtotal", "gst_total", "grand_total"):
            assert k in s
