from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_created_for_each_sale_line_item():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 2:
        return
    p1, p2 = products[0], products[1]
    # Count existing movements
    before = client.get("/inventory/movements").json()
    before_count = len(before)

    sale = client.post("/sales", json={
        "customer_name": "MovementsPerLine",
        "line_items": [
            {"product_id": p1["id"], "qty": 1},
            {"product_id": p2["id"], "qty": 2},
        ]
    })
    assert sale.status_code in (200, 201), sale.text

    after = client.get("/inventory/movements").json()
    assert len(after) >= before_count + 2
