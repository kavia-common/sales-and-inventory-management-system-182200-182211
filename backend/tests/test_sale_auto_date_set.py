from fastapi.testclient import TestClient
from src.api.main import app
from datetime import datetime

client = TestClient(app)

def test_sale_date_is_auto_set_when_omitted():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    resp = client.post("/sales", json={
        "customer_name": "AutoDate",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    # Validate ISO-like timestamp parseability
    assert "date" in sale
    # datetime.fromisoformat allows 'YYYY-MM-DDTHH:MM:SS[.fffff][+HH:MM]'
    datetime.fromisoformat(sale["date"].replace("Z", "+00:00"))
