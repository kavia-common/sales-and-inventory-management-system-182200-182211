from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_price_rounds_to_two_decimals_on_update_and_persist():
    # Create
    r = client.post("/products", json={
        "name": "RoundPersist",
        "sku": "ROUND-PERSIST-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Update with many decimals
    up = client.put(f"/products/{pid}", json={"price": 12.34567})
    assert up.status_code == 200, up.text
    body = up.json()
    assert Decimal(str(body["price"])) == Decimal("12.35")

    # Fetch and confirm persistence
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert Decimal(str(g.json()["price"])) == Decimal("12.35")
