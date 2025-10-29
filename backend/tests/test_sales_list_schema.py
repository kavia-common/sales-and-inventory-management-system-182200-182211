from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_returns_list_and_line_items_present():
    client.post("/seed")
    products = client.get("/products").json()
    if products:
        pid = products[0]["id"]
        client.post("/sales", json={"customer_name": "ListSchema", "line_items": [{"product_id": pid, "qty": 1}]})
    r = client.get("/sales")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert "line_items" in data[0]
