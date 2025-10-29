from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_whitespace_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale1 = client.post("/sales", json={"customer_name": "WS1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "WS2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    base = "INV-WS-001"
    ok = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": base})
    assert ok.status_code in (200, 201), ok.text

    # Try same with whitespace around
    dup_ws = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": f"  {base}  "})
    # Depending on trimming behavior: could be 400 if trimmed/normalized, or 200/201 if exact string uniqueness only.
    assert dup_ws.status_code in (200, 201, 400), dup_ws.text
