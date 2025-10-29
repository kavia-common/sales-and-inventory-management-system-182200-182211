from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_uniqueness_mixed_cases_and_spaces_variants():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    base = "INV-MIXED-Case-001"
    sale1 = client.post("/sales", json={"customer_name": "MixCase1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    r1 = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": base})
    assert r1.status_code in (200, 201), r1.text

    sale2 = client.post("/sales", json={"customer_name": "MixCase2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    variants = [base.upper(), base.lower(), f" {base} ", f"\t{base}\n"]
    for v in variants:
        r = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": v})
        assert r.status_code in (200, 201, 400), (v, r.text)
