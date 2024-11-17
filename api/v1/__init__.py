from fastapi import APIRouter

from .health.health import health_router
from .tasks.tasks import task_router

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
