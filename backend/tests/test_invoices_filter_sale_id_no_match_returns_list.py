from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_sale_id_no_match_returns_list():
    r = client.get("/invoices", params={"sale_id": 0})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
