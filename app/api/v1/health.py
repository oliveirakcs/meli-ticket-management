"""Health module"""

from fastapi import APIRouter
from starlette.responses import Response

from app.infrastructure.database import SessionLocal

db = SessionLocal()

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/", status_code=204)
async def health():
    """Endpoint for checking the health of the API.

    Returns:
        Response: A response indicating the health status with a status code of 204 (No Content).
    """
    return Response(status_code=204)
