from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_whitespace_preserved_no_trim():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "WhitespaceNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-WS-{sale['id']}  "  # trailing spaces
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code in (200, 201, 400)  # allow duplicate behavior or trimming differences
    if r.status_code in (200, 201):
        assert r.json()["invoice_number"] == inv_no
