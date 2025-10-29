from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_reason_includes_sale_reference():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "ReasonRef", "line_items": [{"product_id": pid, "qty": 2}]}).json()
    sale_id = sale["id"]
    moves = client.get("/inventory/movements").json()
    # Find at least one movement with "Sale #<id>"
    assert any(f"Sale #{sale_id}" in m.get("reason", "") for m in moves)
