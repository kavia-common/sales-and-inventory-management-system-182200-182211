from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_requires_customer_name():
    # Create product
    p = client.post("/products", json={
        "name": "CustNameReq",
        "sku": "CUST-NAME-REQ-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()

    # Missing customer_name
    r = client.post("/sales", json={
        "line_items": [{"product_id": p["id"], "qty": 1}]
    })
    assert r.status_code in (400, 422)
