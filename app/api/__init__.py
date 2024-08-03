"""This module defines the API routers for the application."""

from fastapi import APIRouter

from app.api.v1.health import health_router
from app.api.v1.routers.users import router as user_router
from app.api.v1.routers.auth import router as auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(user_router)
