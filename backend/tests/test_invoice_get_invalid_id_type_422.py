from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_invalid_id_type_422():
    r = client.get("/invoices/not-an-int")
    # FastAPI returns 422 for path parameter type mismatch
    assert r.status_code in (404, 422)
