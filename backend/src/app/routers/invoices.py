from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.app.db import get_db
from src.app import models, schemas

router = APIRouter()


# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.InvoiceOut, summary="Create invoice from sale", description="Generate an invoice from a sale with totals mirrored from the sale.", responses={400: {"description": "Invoice exists or number duplicate"}, 404: {"description": "Sale not found"}, 422: {"description": "Validation error"}})
def create_invoice(payload: schemas.InvoiceCreateFromSale, db: Session = Depends(get_db)):
    """This is a public function."""
    sale = db.query(models.Sale).get(payload.sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    existing_number = db.query(models.Invoice).filter(models.Invoice.invoice_number == payload.invoice_number).first()
    if existing_number:
        raise HTTPException(status_code=400, detail="Invoice number already exists")

    existing_for_sale = db.query(models.Invoice).filter(models.Invoice.sale_id == sale.id).first()
    if existing_for_sale:
        raise HTTPException(status_code=400, detail="Invoice already exists for this sale")

    invoice = models.Invoice(
        sale_id=sale.id,
        invoice_number=payload.invoice_number,
        date=sale.date,
        billing_address=payload.billing_address,
        gstin=payload.gstin,
        subtotal=sale.subtotal,
        gst_total=sale.gst_total,
        grand_total=sale.grand_total,
    )
    db.add(invoice)
    db.flush()
    db.refresh(invoice)
    return invoice


# PUBLIC_INTERFACE
@router.get(
    "/",
    summary="List invoices",
    description="List invoices, optionally filter by invoice_number or sale_id",
    response_model=list[schemas.InvoiceOut],
)
def list_invoices(
    invoice_number: str | None = Query(None),
    sale_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    """This is a public function."""
    q = db.query(models.Invoice)
    if invoice_number:
        q = q.filter(models.Invoice.invoice_number == invoice_number)
    if sale_id:
        q = q.filter(models.Invoice.sale_id == sale_id)
    return q.order_by(models.Invoice.id.desc()).all()


# PUBLIC_INTERFACE
@router.get("/{invoice_id}", response_model=schemas.InvoiceOut, summary="Get invoice by ID", description="Get a single invoice by ID")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """This is a public function."""
    inv = db.query(models.Invoice).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv
