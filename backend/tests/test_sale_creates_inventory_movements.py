from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_creates_negative_inventory_movements():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create a sale with qty 3
    sale_resp = client.post("/sales", json={
        "customer_name": "Movement Tester",
        "line_items": [{"product_id": pid, "qty": 3}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    # Verify movements list contains an entry for this sale with -3
    moves_resp = client.get("/inventory/movements")
    assert moves_resp.status_code == 200
    moves = moves_resp.json()
    assert any(m["reason"] == f"Sale #{sale_id}" and m["product_id"] == pid and m["change_qty"] == -3 for m in moves)
