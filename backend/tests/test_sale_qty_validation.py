from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_item_qty_must_be_positive():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Zero qty
    r0 = client.post("/sales", json={
        "customer_name": "Qty Test",
        "line_items": [{"product_id": pid, "qty": 0}]
    })
    assert r0.status_code == 422

    # Negative qty
    rneg = client.post("/sales", json={
        "customer_name": "Qty Test",
        "line_items": [{"product_id": pid, "qty": -1}]
    })
    assert rneg.status_code == 422
