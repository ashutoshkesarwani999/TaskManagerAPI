from fastapi import APIRouter

from .health import health_router

health_routers = APIRouter()
health_routers.include_router(
    health_router,
    tags=["health"],
)
__all__ = ["health_routers"]
