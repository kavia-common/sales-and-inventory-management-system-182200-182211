from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_latest_inventory_movement_is_reflected_in_listing():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Post multiple movements
    for reason, delta in [("Initial Add", 2), ("Minor Loss", -1), ("New Shipment", 5)]:
        r = client.post("/inventory/movements", json={
            "product_id": pid,
            "change_qty": delta,
            "reason": reason
        })
        assert r.status_code in (200, 201), r.text

    # Ensure listing contains the last reason "New Shipment"
    lst = client.get("/inventory/movements")
    assert lst.status_code == 200
    data = lst.json()
    assert any(m["product_id"] == pid and m["reason"] == "New Shipment" for m in data)
