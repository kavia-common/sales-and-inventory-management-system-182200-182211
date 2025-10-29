from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_validation_and_trim():
    # Create base product
    r = client.post("/products", json={
        "name": " ToTrim ",
        "sku": "UPD-TRIM-1",
        "price": 12.50,
        "gst_rate": 5.00,
        "stock_qty": 3
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()

    # Update with leading/trailing whitespace and invalid (negative) price rejected
    r_bad = client.put(f"/products/{prod['id']}", json={"price": -1})
    assert r_bad.status_code in (400, 422)

    # Valid trim update
    r_ok = client.put(f"/products/{prod['id']}", json={"name": "  New Name  ", "sku": "  UPD-TRIM-1 "})
    assert r_ok.status_code == 200, r_ok.text
    data = r_ok.json()
    assert data["name"] == "  New Name  ".strip()
    assert data["sku"] == "  UPD-TRIM-1 ".strip()
