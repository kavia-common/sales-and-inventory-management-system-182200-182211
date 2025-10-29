from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_after_empty_filter_still_works():
    # First, apply a filter that should return empty
    empty = client.get("/invoices", params={"invoice_number": "INV-NOT-EXIST-XYZ"})
    assert empty.status_code == 200
    assert isinstance(empty.json(), list)
    assert len(empty.json()) == 0

    # Then, call list without filters; should still succeed and return a list
    lst = client.get("/invoices")
    assert lst.status_code == 200
    assert isinstance(lst.json(), list)
