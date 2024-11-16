from fastapi import APIRouter

from .tasks.tasks import task_router
from .health.health import health_router

v1_router = APIRouter()
v1_router.include_router(
    task_router,
    prefix="/tasks",
    tags=["Tasks"],
)
v1_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)