from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from .db import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    gst_rate = Column(Numeric(5, 2), nullable=False, default=0)  # percentage, e.g., 18.00
    stock_qty = Column(Integer, nullable=False, default=0)

    inventory_movements = relationship("InventoryMovement", back_populates="product")
    sale_line_items = relationship("SaleLineItem", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    customer_name = Column(String(255), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    gst_total = Column(Numeric(12, 2), nullable=False, default=0)
    grand_total = Column(Numeric(12, 2), nullable=False, default=0)

    line_items = relationship("SaleLineItem", back_populates="sale", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="sale", uselist=False)


class SaleLineItem(Base):
    __tablename__ = "sale_line_items"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    gst_rate = Column(Numeric(5, 2), nullable=False)
    line_subtotal = Column(Numeric(12, 2), nullable=False)
    line_gst = Column(Numeric(12, 2), nullable=False)
    line_total = Column(Numeric(12, 2), nullable=False)

    sale = relationship("Sale", back_populates="line_items")
    product = relationship("Product", back_populates="sale_line_items")

    __table_args__ = (
        Index("idx_sale_product", "sale_id", "product_id"),
    )


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    change_qty = Column(Integer, nullable=False)  # positive or negative
    reason = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    product = relationship("Product", back_populates="inventory_movements")

    __table_args__ = (
        Index("idx_product_timestamp", "product_id", "timestamp"),
    )


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    invoice_number = Column(String(100), unique=True, nullable=False, index=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    billing_address = Column(String(500), nullable=True)
    gstin = Column(String(50), nullable=True)
    subtotal = Column(Numeric(12, 2), nullable=False)
    gst_total = Column(Numeric(12, 2), nullable=False)
    grand_total = Column(Numeric(12, 2), nullable=False)

    sale = relationship("Sale", back_populates="invoice")
