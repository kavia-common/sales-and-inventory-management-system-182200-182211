from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_multiple_list_queries_are_consistent():
    client.post("/seed")
    # First list
    r1 = client.get("/invoices")
    assert r1.status_code == 200
    first = r1.json()
    assert isinstance(first, list)

    # Second list - should not error and should be list
    r2 = client.get("/invoices")
    assert r2.status_code == 200
    second = r2.json()
    assert isinstance(second, list)
    # Count should be >= previous count (other tests may create more invoices)
    assert len(second) >= len(first)
