from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_by_number():
    client.post("/seed")
    # Create product and sale quickly if none
    products = client.get("/products").json()
    if not products:
        p = client.post("/products", json={"name":"Temp","sku":"INV-BY-NUM-1","price":10.0,"gst_rate":5.0,"stock_qty":10}).json()
        pid = p["id"]
    else:
        pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "ByNumber",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    inv_no = f"INV-BYNUM-{sale['id']}"
    r_create = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r_create.status_code in (200, 201), r_create.text

    r = client.get(f"/invoices/number/{inv_no}")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["invoice_number"] == inv_no

    r_missing = client.get("/invoices/number/DOES-NOT-EXIST-12345")
    assert r_missing.status_code == 404
