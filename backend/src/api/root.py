from fastapi import APIRouter

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", tags=["health"], summary="Root endpoint", description="Root endpoint returning service status message.")
def root_status():
    """This is a public function."""
    return {"message": "Healthy"}
