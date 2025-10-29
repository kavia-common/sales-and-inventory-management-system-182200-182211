import os
from fastapi import APIRouter

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/info", tags=["health"], summary="Service info", description="Basic service metadata and non-sensitive configuration")
def service_info():
    """This is a public function."""
    return {
        "name": "Sales & Inventory Management API",
        "version": "1.0.0",
        "cors_allow_origins": [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")] if os.getenv("CORS_ALLOW_ORIGINS") else ["*"],
        "db_host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "db_port": os.getenv("MYSQL_PORT", "5001"),
        "db_name": os.getenv("MYSQL_DB", "sales_inventory_db"),
    }
