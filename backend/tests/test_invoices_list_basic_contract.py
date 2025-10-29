from fastapi.testclient import TestClient
from src.api.main import app

def test_invoices_list_basic_contract():
    client = TestClient(app)
    client.post("/seed")
    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # Slicing client-side should not error
    _ = data[:5]
