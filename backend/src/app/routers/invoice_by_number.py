from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from src.app.db import get_db
from src.app import models, schemas

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/{invoice_number}", response_model=schemas.InvoiceOut, summary="Get invoice by number", description="Fetch a single invoice using its unique invoice number")
def get_by_number(invoice_number: str = Path(..., description="Invoice number"), db: Session = Depends(get_db)):
    """This is a public function."""
    inv = db.query(models.Invoice).filter(models.Invoice.invoice_number == invoice_number).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv
