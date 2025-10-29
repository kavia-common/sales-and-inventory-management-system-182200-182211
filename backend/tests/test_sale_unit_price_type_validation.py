from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_unit_price_must_be_numeric_type():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    # Pass a string for unit_price to trigger validation error
    r = client.post("/sales", json={
        "customer_name": "TypeValidation",
        "line_items": [{"product_id": pid, "qty": 1, "unit_price": "ten"}]
    })
    assert r.status_code in (400, 422)
