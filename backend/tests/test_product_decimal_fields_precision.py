from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_decimal_fields_precision():
    r = client.post("/products", json={
        "name": "DecimalCheck",
        "sku": "DEC-CHK-1",
        "price": 12.345,
        "gst_rate": 7.895,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201, 422), r.text
    if r.status_code in (200, 201):
        p = r.json()
        # Returned decimals should be parseable and at 2dp
        price = Decimal(str(p["price"]))
        gst = Decimal(str(p["gst_rate"]))
        assert price == price.quantize(Decimal("0.01"))
        assert gst == gst.quantize(Decimal("0.01"))
