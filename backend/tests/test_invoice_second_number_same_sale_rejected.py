from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_second_number_same_sale_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "SecondNum",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    inv_no1 = f"INV-SECOND-{sale['id']}-A"
    inv_no2 = f"INV-SECOND-{sale['id']}-B"

    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no1})
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no2})
    assert r2.status_code == 400
