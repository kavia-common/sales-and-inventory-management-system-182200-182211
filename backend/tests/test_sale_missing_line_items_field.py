from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_missing_line_items_field_rejected():
    r = client.post("/sales", json={"customer_name": "NoItemsField"})
    assert r.status_code in (400, 422)
