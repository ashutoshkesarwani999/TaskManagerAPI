from fastapi import APIRouter

from .tasks import task_router

tasks_router = APIRouter()
tasks_router.include_router(
    task_router,
    tags=["Tasks"],
)

__all__ = ["tasks_router"]