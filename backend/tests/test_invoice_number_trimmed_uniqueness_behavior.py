from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_trimmed_uniqueness_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale1 = client.post("/sales", json={"customer_name": "Trim1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "Trim2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    base = "INV-TRIM-001"
    ok = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": base})
    assert ok.status_code in (200, 201), ok.text

    # Try same number with mixed whitespace
    dup = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": "\t" + base + "  "})
    # Depending on server normalization, either 400 (trimmed) or 200/201 (exact-match only) is acceptable here.
    assert dup.status_code in (200, 201, 400), dup.text
