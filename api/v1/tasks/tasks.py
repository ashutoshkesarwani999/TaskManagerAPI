from fastapi import APIRouter, Request
from typing import List, Union
from app.schemas.response import (
    TaskResponse,
    sampleListTaskResponse,
    sampleTaskResponse,
)

task_router = APIRouter()


@task_router.post(
    "/",
    summary="Create Task",
    description="Create Task",
    tags=["Tasks"],
    status_code=201,
    response_description="Successful Response",
)
async def create_task(
    request: Request,
    task_create: dict,
) -> TaskResponse:
    return sampleTaskResponse.get(200)


@task_router.get(
    "/",
    summary="List all Tasks",
    description="List all Tasks",
    tags=["Tasks"],
    status_code=200,
)
async def get_tasks(request: Request) -> List[TaskResponse]:

    return sampleListTaskResponse.get(200)


@task_router.get(
    "/{task_id}",
    summary="List single Task",
    description="List single Task",
    tags=["Tasks"],
    status_code=200,
)
async def get_tasks(task_id: Union[int, str]) -> TaskResponse:
    print("task__id",task_id)
    return sampleTaskResponse.get(200)


@task_router.put(
    "/{task_id}",
    summary="Update Task",
    description="Update Task",
    tags=["Tasks"],
    status_code=200,
)
async def update_task(
    request: Request,
    task_update: dict,
) -> TaskResponse:

    return {
        "id": 1,
        "title": "Buy Groceries",
        "description": "Milk, Eggs, Bread, Butter",
        "completed": False,
        "created_at": "2024-11-16T14:30:00",
    }


@task_router.delete(
    "/{task_id}",
    summary="Delete Task",
    description="Delete Task",
    tags=["Tasks"],
    status_code=204,
)
async def get_task(
    task_id: Union[int, str],
):

    return
