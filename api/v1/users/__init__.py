from fastapi import APIRouter

from .users import user_router

tasks_router = APIRouter()
tasks_router.include_router(
    user_router,
    tags=["Users"],
)

__all__ = ["users_router"]
