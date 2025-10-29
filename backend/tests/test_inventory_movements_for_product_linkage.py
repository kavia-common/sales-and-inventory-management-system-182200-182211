from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_linked_to_correct_product_id():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]

    client.post("/inventory/movements", json={"product_id": pid1, "change_qty": 2, "reason": "Prod1Add"})
    client.post("/inventory/movements", json={"product_id": pid2, "change_qty": 3, "reason": "Prod2Add"})

    lst = client.get("/inventory/movements")
    assert lst.status_code == 200
    data = lst.json()
    assert any(m["product_id"] == pid1 for m in data)
    assert any(m["product_id"] == pid2 for m in data)
