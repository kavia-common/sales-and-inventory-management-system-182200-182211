from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_returns_list_type_even_empty():
    r = client.get("/invoices")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
