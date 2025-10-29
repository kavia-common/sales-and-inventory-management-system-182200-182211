from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_partial_persistence_is_not_allowed():
    # Create a valid product
    p = client.post("/products", json={
        "name": "PartialGuard",
        "sku": "PART-GUARD-1",
        "price": 5.0,
        "gst_rate": 5.0,
        "stock_qty": 10
    }).json()

    # Attempt sale with one valid and one invalid product_id
    r = client.post("/sales", json={
        "customer_name": "Partial",
        "line_items": [
            {"product_id": p["id"], "qty": 1},
            {"product_id": 999999999, "qty": 1}
        ]
    })
    assert r.status_code == 404

    # Ensure inventory did not decrement for the valid product
    p_after = client.get(f"/products/{p['id']}").json()
    assert int(p_after["stock_qty"]) == 10
