import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.app.db import init_db
from src.api.error_handlers import unhandled_exception_handler
from src.api.register_routes import register_app_routes
from src.api.register_startup import register_startup_hooks

load_dotenv()

app = FastAPI(
    title="Sales & Inventory Management API",
    description="Backend service for products, inventory movements, sales with GST calculations, and invoices.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoint and utilities"},
        {"name": "products", "description": "Manage products and stock quantity"},
        {"name": "inventory", "description": "Record and view inventory movements"},
        {"name": "sales", "description": "Create and view sales with GST calculations"},
        {"name": "invoices", "description": "Generate and view invoices from sales"},
    ],
)

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
    init_db()

app.add_exception_handler(Exception, unhandled_exception_handler)

register_app_routes(app)
register_startup_hooks(app)
