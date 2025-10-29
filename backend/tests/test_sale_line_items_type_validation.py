from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_items_must_be_list():
    # Create a product for reference
    p = client.post("/products", json={
        "name": "TypeValProd",
        "sku": "TYPE-VAL-001",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()

    # Pass dict instead of list for line_items -> expect 422/400
    r = client.post("/sales", json={
        "customer_name": "BadLineItemsType",
        "line_items": {"product_id": p["id"], "qty": 1}
    })
    assert r.status_code in (400, 422)
