from fastapi.testclient import TestClient
from src.api.main import app
from datetime import datetime, timezone

client = TestClient(app)

def test_sale_explicit_date_is_preserved():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    explicit = datetime(2024, 5, 1, 10, 30, 0, tzinfo=timezone.utc).isoformat()
    resp = client.post("/sales", json={
        "customer_name": "ExplicitDate",
        "date": explicit,
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    assert "date" in sale
    # Normalize potential 'Z'
    got = sale["date"].replace("Z", "+00:00")
    assert got.startswith("2024-05-01T10:30:00")
