from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_get_by_id_returns_expected_fields_and_types():
    r = client.post("/products", json={
        "name": "FieldCheck",
        "sku": "FIELD-CHK-1",
        "price": 33.21,
        "gst_rate": 18.0,
        "stock_qty": 7
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    body = g.json()
    assert set(["id", "name", "sku", "price", "gst_rate", "stock_qty"]).issubset(body.keys())
    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["sku"], str)
    # price/gst_rate may be serialized as str or float; just ensure presence is handled above
    assert isinstance(body["stock_qty"], int)
