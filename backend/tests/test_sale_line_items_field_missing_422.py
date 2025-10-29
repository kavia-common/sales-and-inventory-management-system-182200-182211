from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_missing_line_items_field_returns_error():
    client.post("/seed")
    r = client.post("/sales", json={
        "customer_name": "MissingItemsField"
    })
    assert r.status_code in (400, 422)
