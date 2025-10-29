from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_with_non_numeric_price_rejected():
    # Create a product
    r = client.post("/products", json={
        "name": "TypeValProd",
        "sku": "TYPE-VAL-001",
        "price": 9.99,
        "gst_rate": 12.0,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Attempt to update price with a non-numeric string
    up = client.put(f"/products/{pid}", json={"price": "not-a-number"})
    assert up.status_code in (400, 422)
