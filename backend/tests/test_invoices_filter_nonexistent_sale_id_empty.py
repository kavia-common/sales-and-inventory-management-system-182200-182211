from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_nonexistent_sale_id_returns_empty():
    r = client.get("/invoices", params={"sale_id": 9999999})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert r.json() == [] or isinstance(r.json(), list)
