from decimal import Decimal, ROUND_HALF_UP
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.db import get_db
from src.app import models, schemas

router = APIRouter()


def money(x: Decimal) -> Decimal:
    return (x or Decimal("0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.SaleOut, summary="Create sale", description="Create a sale with line items. Calculates GST per line and totals and decrements inventory.")
def create_sale(payload: schemas.SaleCreate, db: Session = Depends(get_db)):
    """This is a public function."""
    if not payload.line_items:
        raise HTTPException(status_code=400, detail="No line items provided")

    sale = models.Sale(
        customer_name=payload.customer_name,
        date=payload.date,
    )
    db.add(sale)
    db.flush()  # get sale.id for line items

    subtotal = Decimal("0.00")
    gst_total = Decimal("0.00")
    line_objects: List[models.SaleLineItem] = []

    # Validate stock and compute amounts
    for li in payload.line_items:
        product = db.query(models.Product).get(li.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {li.product_id} not found")
        if int(product.stock_qty) < int(li.qty):
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.sku}")

        unit_price = Decimal(str(li.unit_price)) if li.unit_price is not None else Decimal(str(product.price))
        gst_rate = Decimal(str(li.gst_rate)) if li.gst_rate is not None else Decimal(str(product.gst_rate))

        line_subtotal = money(unit_price * Decimal(int(li.qty)))
        line_gst = money(line_subtotal * gst_rate / Decimal("100"))
        line_total = money(line_subtotal + line_gst)

        subtotal += line_subtotal
        gst_total += line_gst

        line_obj = models.SaleLineItem(
            sale_id=sale.id,
            product_id=product.id,
            qty=int(li.qty),
            unit_price=money(unit_price),
            gst_rate=money(gst_rate),
            line_subtotal=money(line_subtotal),
            line_gst=money(line_gst),
            line_total=money(line_total),
        )
        line_objects.append(line_obj)

    # Persist line items and update stock with an inventory movement per item
    for li_obj in line_objects:
        db.add(li_obj)
        # decrement stock
        product = db.query(models.Product).get(li_obj.product_id)
        product.stock_qty = int(product.stock_qty) - int(li_obj.qty)
        db.add(models.InventoryMovement(
            product_id=li_obj.product_id,
            change_qty=-int(li_obj.qty),
            reason=f"Sale #{sale.id}",
        ))
        db.add(product)

    sale.subtotal = money(subtotal)
    sale.gst_total = money(gst_total)
    sale.grand_total = money(subtotal + gst_total)

    db.add(sale)
    db.flush()
    db.refresh(sale)

    return sale


# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.SaleOut], summary="List sales", description="List all sales with line items")
def list_sales(db: Session = Depends(get_db)):
    """This is a public function."""
    sales = db.query(models.Sale).order_by(models.Sale.id.desc()).all()
    # Eager load line items through ORM relationship when returned
    return sales


# PUBLIC_INTERFACE
@router.get("/{sale_id}", response_model=schemas.SaleOut, summary="Get sale", description="Get a sale by ID")
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """This is a public function."""
    sale = db.query(models.Sale).get(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
