from fastapi.testclient import TestClient
from src.api.main import app
from datetime import datetime

client = TestClient(app)

def test_inventory_movement_timestamp_is_iso_like():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    mv = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "TS"}).json()
    assert "timestamp" in mv
    # Parse ISO-like format (normalize potential Z)
    datetime.fromisoformat(mv["timestamp"].replace("Z", "+00:00"))
