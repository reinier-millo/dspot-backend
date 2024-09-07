from fastapi import APIRouter
from app.constants import API_VERSION
from app.models.health import Health

health_router = APIRouter()


@health_router.get("/", response_model=Health, status_code=200)
def health() -> Health:
    """
    Health check endpoint
    """
    return Health(status="ok", version=API_VERSION)
