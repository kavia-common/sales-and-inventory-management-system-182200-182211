from datetime import datetime, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_explicit_date_is_persisted():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    explicit_dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc).isoformat()
    resp = client.post("/sales", json={
        "customer_name": "ExplicitDate",
        "date": explicit_dt,
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    # Compare up to seconds
    assert sale["date"][:19] == explicit_dt[:19]
