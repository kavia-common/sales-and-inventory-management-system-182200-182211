from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_creates_one_inventory_movement_per_line_item():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]

    # Count movements before
    before = client.get("/inventory/movements").json()
    before_count = len(before)

    sale_resp = client.post("/sales", json={
        "customer_name": "MovementsPerLine",
        "line_items": [
            {"product_id": pid1, "qty": 1},
            {"product_id": pid2, "qty": 2},
        ]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text

    after = client.get("/inventory/movements").json()
    assert len(after) >= before_count + 2
