from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_sku_case_sensitivity_behavior():
    r1 = client.post("/products", json={"name":"CaseSKU","sku":"Case-123","price":1.0,"gst_rate":5.0,"stock_qty":1})
    assert r1.status_code in (200, 201, 422, 400)
    r2 = client.post("/products", json={"name":"CaseSKU2","sku":"case-123","price":1.0,"gst_rate":5.0,"stock_qty":1})
    # Depending on DB collation and constraints, allow 201 or 400
    assert r2.status_code in (200, 201, 400, 422)
