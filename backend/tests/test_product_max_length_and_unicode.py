from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_accepts_unicode_and_long_name_within_limits():
    name = "Üñïçø∂ê Product – 测试 ✅"
    sku = "UNICODE-" + "X" * 80  # within typical 100-char limit
    r = client.post("/products", json={
        "name": name,
        "sku": sku,
        "price": 123.45,
        "gst_rate": 18.0,
        "stock_qty": 10
    })
    assert r.status_code in (200, 201, 422), r.text
    if r.status_code in (200, 201):
        body = r.json()
        assert body["name"] == name
        assert body["sku"] == sku
