from fastapi import FastAPI, Query
from datetime import datetime


# PUBLIC_INTERFACE
def register_invoice_number_route(app: FastAPI) -> None:
    """Register utility endpoint to suggest a unique invoice number format."""
    @app.get("/invoices/next-number", tags=["invoices"], summary="Suggest next invoice number")
    def next_invoice_number(prefix: str = Query("INV", min_length=1, max_length=10)):
        """This is a public function."""
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return {"invoice_number": f"{prefix}-{ts}"}
