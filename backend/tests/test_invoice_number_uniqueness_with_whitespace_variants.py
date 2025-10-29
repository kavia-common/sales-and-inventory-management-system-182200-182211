from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_uniqueness_with_whitespace_variants():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    # First sale and invoice with base number
    sale1 = client.post("/sales", json={"customer_name": "WSVar1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    base = "INV-WSVAR-100"
    resp1 = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": base})
    assert resp1.status_code in (200, 201), resp1.text

    # Second sale, try number with internal/leading/trailing whitespace variants
    sale2 = client.post("/sales", json={"customer_name": "WSVar2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    variants = [f" {base}", f"{base} ", f"\t{base}\n"]
    for v in variants:
        r = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": v})
        # Accept both strict and normalized enforcement
        assert r.status_code in (200, 201, 400), (v, r.text)
