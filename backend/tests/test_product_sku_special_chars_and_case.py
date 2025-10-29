from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_sku_allows_special_chars_and_preserves_case():
    sku = "Sku-Alpha_01/★"
    r = client.post("/products", json={
        "name": "SpecialSKU",
        "sku": sku,
        "price": 12.34,
        "gst_rate": 18.0,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    assert prod["sku"] == sku

    # fetch by ID and confirm case preserved
    g = client.get(f"/products/{prod['id']}")
    assert g.status_code == 200
    assert g.json()["sku"] == sku
