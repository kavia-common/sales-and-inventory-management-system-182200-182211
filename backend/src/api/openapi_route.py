from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Request

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/openapi.json", tags=["health"], summary="OpenAPI schema", description="Return the OpenAPI schema of the service")
def get_openapi_schema(request: Request):
    """This is a public function."""
    return JSONResponse(request.app.openapi())
