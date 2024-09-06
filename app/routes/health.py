from fastapi import APIRouter
from app.constants import API_VERSION

health_router = APIRouter()


@health_router.get("/")
def health() -> dict:
    """
    Health check endpoint
    """
    return {"status": "ok", "version": API_VERSION}
