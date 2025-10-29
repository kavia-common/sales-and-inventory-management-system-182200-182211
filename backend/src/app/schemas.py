from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, validator, constr, condecimal, conint


# Product Schemas
class ProductBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=255) = Field(..., description="Product name")
    sku: constr(strip_whitespace=True, min_length=1, max_length=100) = Field(..., description="Stock keeping unit (unique)")
    price: condecimal(ge=0, max_digits=12, decimal_places=2) = Field(..., description="Base price per unit")
    gst_rate: condecimal(ge=0, le=100, max_digits=5, decimal_places=2) = Field(..., description="GST rate percentage")
    stock_qty: conint(ge=0) = Field(..., description="Current stock quantity")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = Field(None)
    sku: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = Field(None)
    price: Optional[condecimal(ge=0, max_digits=12, decimal_places=2)] = Field(None)
    gst_rate: Optional[condecimal(ge=0, le=100, max_digits=5, decimal_places=2)] = Field(None)
    stock_qty: Optional[conint(ge=0)] = Field(None)


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True


# Inventory Movement Schemas
class InventoryMovementCreate(BaseModel):
    product_id: int = Field(..., description="Product ID")
    change_qty: int = Field(..., description="Positive to add stock; negative to remove")
    reason: constr(strip_whitespace=True, min_length=1, max_length=255) = Field(..., description="Reason for movement")


class InventoryMovementOut(BaseModel):
    id: int
    product_id: int
    change_qty: int
    reason: str
    timestamp: datetime

    class Config:
        from_attributes = True


# Sale and Line Items
class SaleLineItemCreate(BaseModel):
    product_id: int = Field(..., description="Product ID")
    qty: int = Field(..., description="Quantity")
    unit_price: Optional[Decimal] = Field(None, description="Override unit price; default product price")
    gst_rate: Optional[Decimal] = Field(None, description="Override GST rate; default product GST rate")

    @validator("qty")
    def qty_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v


class SaleCreate(BaseModel):
    customer_name: str = Field(..., description="Customer name")
    date: Optional[datetime] = Field(None, description="Sale date; default now")
    line_items: List[SaleLineItemCreate] = Field(..., description="List of sale items")


class SaleLineItemOut(BaseModel):
    id: int
    sale_id: int
    product_id: int
    qty: int
    unit_price: Decimal
    gst_rate: Decimal
    line_subtotal: Decimal
    line_gst: Decimal
    line_total: Decimal

    class Config:
        from_attributes = True


class SaleOut(BaseModel):
    id: int
    date: datetime
    customer_name: str
    subtotal: Decimal
    gst_total: Decimal
    grand_total: Decimal
    line_items: List[SaleLineItemOut]

    class Config:
        from_attributes = True


# Invoice Schemas
class InvoiceCreateFromSale(BaseModel):
    sale_id: int = Field(..., description="Sale ID to generate invoice for")
    invoice_number: str = Field(..., description="Unique invoice number")
    billing_address: Optional[str] = Field(None, description="Billing address")
    gstin: Optional[str] = Field(None, description="Customer GSTIN")


class InvoiceOut(BaseModel):
    id: int
    sale_id: int
    invoice_number: str
    date: datetime
    billing_address: Optional[str]
    gstin: Optional[str]
    subtotal: Decimal
    gst_total: Decimal
    grand_total: Decimal

    class Config:
        from_attributes = True
