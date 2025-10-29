from fastapi.testclient import TestClient
from src.api.main import app

def test_sales_list_smoke():
    client = TestClient(app)
    client.post("/seed")
    # Ensure at least one sale exists
    client.post("/sales", json={"customer_name": "Sales Smoke", "line_items": [{"product_id": 1, "qty": 1}]})
    resp = client.get("/sales")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        sale = data[0]
        for key in ("id", "customer_name", "subtotal", "gst_total", "grand_total", "line_items"):
            assert key in sale
