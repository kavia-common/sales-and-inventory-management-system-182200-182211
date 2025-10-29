from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_future_date_is_accepted():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    future = datetime.now(timezone.utc) + timedelta(days=30)
    future_iso = future.isoformat()
    sale = client.post("/sales", json={
        "customer_name": "FutureDate",
        "date": future_iso,
        "line_items": [{"product_id": products[0]["id"], "qty": 1}]
    })
    assert sale.status_code in (200, 201), sale.text
    assert sale.json()["date"].startswith(future_iso[:19])
