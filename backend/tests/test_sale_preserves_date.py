from datetime import datetime, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_creation_preserves_provided_date():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    dt = datetime(2024, 1, 1, 12, 34, 56, tzinfo=timezone.utc).isoformat()
    r = client.post("/sales", json={
        "customer_name": "DateProvided",
        "date": dt,
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert r.status_code in (200, 201), r.text
    body = r.json()
    # Some servers may truncate to seconds; compare prefix
    assert body["date"].startswith("2024-01-01T12:34:56")
