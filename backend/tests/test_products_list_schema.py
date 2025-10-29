from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_contains_expected_fields_and_types():
    # Ensure at least one product exists
    client.post("/seed")
    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if not data:
        return
    p = data[0]
    for key in ("id", "name", "sku", "price", "gst_rate", "stock_qty"):
        assert key in p
    assert isinstance(p["id"], int)
    assert isinstance(p["name"], str)
    assert isinstance(p["sku"], str)
    # numeric fields are serialized as numbers or strings; convert to Decimal for validation
    Decimal(str(p["price"]))
    Decimal(str(p["gst_rate"]))
    assert isinstance(p["stock_qty"], int)
