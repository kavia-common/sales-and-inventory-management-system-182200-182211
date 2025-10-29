from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_with_special_chars_in_name_and_sku():
    name = "Café Latte – Premium ☕"
    sku = "SKU-Δ-ß-漢字-123"
    r = client.post("/products", json={
        "name": name,
        "sku": sku,
        "price": 12.5,
        "gst_rate": 5.0,
        "stock_qty": 3
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    data = g.json()
    assert data["name"] == name
    assert data["sku"] == sku
