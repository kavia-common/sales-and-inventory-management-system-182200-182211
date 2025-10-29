from fastapi.testclient import TestClient
from src.api.main import app
from datetime import datetime

client = TestClient(app)

def test_invoice_date_field_is_isoformat():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "ISODate", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-ISO-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text

    lst = client.get("/invoices")
    assert lst.status_code == 200
    inv = lst.json()[0]
    # Basic ISO check: parseable by datetime.fromisoformat (strip Z if present)
    date_str = inv["date"]
    try:
        _ = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception as e:
        assert False, f"Invoice date not ISO parseable: {date_str} ({e})"
