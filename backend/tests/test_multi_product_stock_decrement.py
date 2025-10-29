from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_decrements_stock_for_each_product_in_line_items():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]
    stock1_before, stock2_before = int(p1["stock_qty"]), int(p2["stock_qty"])

    qty1, qty2 = 2, 3
    resp = client.post("/sales", json={
        "customer_name": "MultiProductStock",
        "line_items": [
            {"product_id": pid1, "qty": qty1},
            {"product_id": pid2, "qty": qty2}
        ]
    })
    assert resp.status_code in (200, 201), resp.text

    p1_after = client.get(f"/products/{pid1}").json()
    p2_after = client.get(f"/products/{pid2}").json()
    assert int(p1_after["stock_qty"]) == stock1_before - qty1
    assert int(p2_after["stock_qty"]) == stock2_before - qty2
