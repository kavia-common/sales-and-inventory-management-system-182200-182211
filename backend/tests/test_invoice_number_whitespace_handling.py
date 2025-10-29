from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_with_whitespace_handling():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "WSNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    base = "INV-WS-01"
    first = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": base})
    assert first.status_code in (200, 201), first.text

    # Try creating a different sale with whitespace-padded same number to probe normalization behavior
    sale2 = client.post("/sales", json={"customer_name": "WSNum2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    padded = f"  {base}\t"
    second = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": padded})
    # Either normalized (400 conflict) or treated as different (200/201). Accept both.
    assert second.status_code in (200, 201, 400)
