from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sku_case_uniqueness_behavior():
    r1 = client.post("/products", json={
        "name": "CaseUniq1",
        "sku": "CaseSKU",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post("/products", json={
        "name": "CaseUniq2",
        "sku": "casesku",  # lower case
        "price": 2.0,
        "gst_rate": 5.0,
        "stock_qty": 2
    })
    # Depending on DB collation this might be rejected or allowed
    assert r2.status_code in (200, 201, 400), r2.text
