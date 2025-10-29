import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.app.db import init_db
from src.app.routers import products as products_router
from src.app.routers import inventory as inventory_router
from src.app.routers import sales as sales_router
from src.app.routers import invoices as invoices_router
from src.app.routers import seed as seed_router
from src.app.routers import invoice_by_number as invoice_by_number_router

# Load environment variables from .env if present
load_dotenv()

# Create FastAPI app with metadata
app = FastAPI(
    title="Sales & Inventory Management API",
    description="Backend service for products, inventory movements, sales with GST calculations, and invoices.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoint"},
        {"name": "products", "description": "Manage products and stock quantity"},
        {"name": "inventory", "description": "Record and view inventory movements"},
        {"name": "sales", "description": "Create and view sales with GST calculations"},
        {"name": "invoices", "description": "Generate and view invoices from sales"},
        {"name": "seed", "description": "Seed baseline data for quick start"},
    ],
)

# CORS configuration - allow mobile frontend origins; default to permissive if not set
allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
allow_origins = [o.strip() for o in allowed_origins.split(",")] if allowed_origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    Initialize database engine and create tables on startup.
    """
    init_db()


# PUBLIC_INTERFACE
@app.get("/health", tags=["health"], summary="Health check", description="Returns OK if the service is running")
def health_check():
    """This is a public function."""
    return {"status": "OK"}


# Include routers
app.include_router(products_router.router, prefix="/products", tags=["products"])
app.include_router(inventory_router.router, prefix="/inventory", tags=["inventory"])
app.include_router(sales_router.router, prefix="/sales", tags=["sales"])
# /invoices general CRUD/list
app.include_router(invoices_router.router, prefix="/invoices", tags=["invoices"])
# /invoices/number/{invoice_number}
app.include_router(invoice_by_number_router.router, prefix="/invoices/number", tags=["invoices"])
# /seed
app.include_router(seed_router.router, prefix="/seed", tags=["seed"])


# PUBLIC_INTERFACE
@app.get("/docs/websocket-usage", tags=["health"], summary="WebSocket usage note")
def websocket_usage_note():
    """This is a public function."""
    return {"note": "No WebSocket endpoints in this project."}
