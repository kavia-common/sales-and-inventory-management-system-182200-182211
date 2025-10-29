from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from src.app.db import get_db
from src.app import models, schemas

router = APIRouter()


# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.ProductOut, summary="Create product", description="Create a new product with initial stock", responses={400: {"description": "Duplicate SKU"}, 422: {"description": "Validation error"}})
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """This is a public function."""
    existing = db.query(models.Product).filter(models.Product.sku == product.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    obj = models.Product(
        name=product.name.strip(),
        sku=product.sku.strip(),
        price=product.price,
        gst_rate=product.gst_rate,
        stock_qty=product.stock_qty,
    )
    db.add(obj)
    db.flush()
    db.refresh(obj)
    return obj


# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.ProductOut], summary="List products", description="List all products")
def list_products(db: Session = Depends(get_db)):
    """This is a public function."""
    return db.query(models.Product).order_by(models.Product.id.desc()).all()


# PUBLIC_INTERFACE
@router.get("/paged", response_model=List[schemas.ProductOut], summary="List products (paged)", description="List products with offset/limit pagination")
def list_products_paged(
    offset: int = Query(0, ge=0, description="Starting offset"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    db: Session = Depends(get_db),
):
    """This is a public function."""
    q = db.query(models.Product).order_by(models.Product.id.desc()).offset(offset).limit(limit)
    return q.all()


# PUBLIC_INTERFACE
@router.get("/{product_id}", response_model=schemas.ProductOut, summary="Get product", description="Get a product by ID")
def get_product(product_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """This is a public function."""
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


# PUBLIC_INTERFACE
@router.put("/{product_id}", response_model=schemas.ProductOut, summary="Update product", description="Update product fields")
def update_product(product_id: int, payload: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """This is a public function."""
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    # Handle SKU duplicate
    if payload.sku and payload.sku != obj.sku:
        sku_exists = db.query(models.Product).filter(models.Product.sku == payload.sku).first()
        if sku_exists:
            raise HTTPException(status_code=400, detail="SKU already exists")
        obj.sku = payload.sku
    if payload.name is not None:
        obj.name = payload.name.strip()
    if payload.price is not None:
        obj.price = payload.price
    if payload.gst_rate is not None:
        obj.gst_rate = payload.gst_rate
    if payload.stock_qty is not None:
        obj.stock_qty = payload.stock_qty
    db.add(obj)
    db.flush()
    db.refresh(obj)
    return obj


# PUBLIC_INTERFACE
@router.delete("/{product_id}", status_code=204, summary="Delete product", description="Delete a product by ID", responses={204: {"description": "Deleted"}, 404: {"description": "Not found"}})
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """This is a public function."""
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(obj)
    # Return 204 No Content by returning None with status_code on decorator
    return None
