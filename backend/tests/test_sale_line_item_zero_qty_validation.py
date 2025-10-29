from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_item_zero_qty_validation():
    # zero qty should trigger 422 from Pydantic validator
    r = client.post("/sales", json={
        "customer_name": "ZeroQty",
        "line_items": [{"product_id": 1, "qty": 0}]
    })
    assert r.status_code == 422
