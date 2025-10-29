from fastapi import APIRouter

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/routes", tags=["health"], summary="Routes overview", description="List of primary API route groups")
def routes_overview():
    """This is a public function."""
    return {
        "health": ["/health", "/info", "/docs/websocket-usage", "/routes", "/seed"],
        "products": ["/products"],
        "inventory": ["/inventory/movements"],
        "sales": ["/sales"],
        "invoices": ["/invoices"],
    }
