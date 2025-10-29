from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.app.db import get_db
from src.app import models, schemas

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/paged", response_model=List[schemas.ProductOut], summary="List products (paged)", description="List products with offset/limit pagination.")
def list_products_paged(
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Limit for pagination"),
    db: Session = Depends(get_db),
):
    """This is a public function."""
    q = db.query(models.Product).order_by(models.Product.id.desc())
    return q.offset(offset).limit(limit).all()
