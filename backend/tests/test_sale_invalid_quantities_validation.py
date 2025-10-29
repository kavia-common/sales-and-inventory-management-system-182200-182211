from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_item_qty_zero_or_negative_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Zero quantity
    r0 = client.post("/sales", json={
        "customer_name": "InvalidQtyZero",
        "line_items": [{"product_id": pid, "qty": 0}]
    })
    assert r0.status_code in (400, 422)

    # Negative quantity
    rn = client.post("/sales", json={
        "customer_name": "InvalidQtyNeg",
        "line_items": [{"product_id": pid, "qty": -1}]
    })
    assert rn.status_code in (400, 422)
