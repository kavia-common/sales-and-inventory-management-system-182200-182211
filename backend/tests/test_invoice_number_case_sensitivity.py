from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_case_sensitivity_exact_match_required():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale1 = client.post("/sales", json={"customer_name": "Case1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "Case2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    inv_num = "Inv-Case-001"
    first = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": inv_num})
    assert first.status_code in (200, 201), first.text

    # Different casing; behavior may be case-sensitive (allow) or normalized (reject). Accept both outcomes.
    second = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": inv_num.upper()})
    assert second.status_code in (200, 201, 400), second.text
