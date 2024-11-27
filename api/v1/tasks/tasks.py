from typing import List, Optional, Union

from fastapi import APIRouter, Body, Depends, Path, Query, Request, status
from app.controllers.task import TaskController
from app.schemas.exceptions import (
    DatabaseError,
    InvalidFormatError,
    NotFoundError,
    UniqueConstraintViolation,
)
from app.schemas.request import TaskCreateRequest, TaskUpdateRequest
from app.schemas.response import TaskResponse
from core.exceptions import BadRequestException
from core.factory.factory import Factory
from core.security.limiter import limiter

task_router = APIRouter()


@task_router.post(
    "/",
    summary="Create New Task",
    description="""
    Create a new task with the provided details.
    
    This endpoint allows you to:
    * Create a new task
    * Set completion status
    * Provide task description
    """,
    tags=["Tasks"],
    status_code=status.HTTP_201_CREATED,
    response_description="Task created successfully",
    response_model=TaskResponse,
    responses={
        422: {
            "model": UniqueConstraintViolation,
            "description": "Task ID already exists",
        },
        500: {"model": DatabaseError, "description": "Database error occured"},
    },
)
async def create_task(
    request: Request,
    task_create: TaskCreateRequest = Body(..., description="Task data to create"),
    task_controller: TaskController = Depends(Factory().get_task_controller),
) -> TaskResponse:
    """
    Create a new task.

    This endpoint creates a new task with the provided details. The task ID must
    be a positive integer, and the title is required.

    Args:
        request (Request): The incoming request
        task_create (TaskCreateRequest): The task data to create
        task_controller (TaskController): The task controller instance

    Returns:
        TaskResponse: The created task

    Raises:
        BadRequestException: If the task ID is not positive
        ValidationError: If required fields are missing
    """
    task = await task_controller.create(attributes=task_create.model_dump())
    return task


@task_router.get(
    "/",
    summary="List All Tasks",
    description="""
    Retrieve a list of all tasks with optional pagination.
    
    This endpoint allows you to:
    * Get all tasks
    * Paginate results
    * Filter completed/incomplete tasks
    """,
    tags=["Tasks"],
    status_code=status.HTTP_200_OK,
    response_description="List of tasks retrieved successfully",
    response_model=List[TaskResponse],
    responses={500: {"model": DatabaseError, "description": "Database error occured"}},
)
@limiter.limit("2/minute")
async def get_tasks(
    request: Request,
    skip: int = Query(
        default=0, ge=0, description="Number of tasks to skip (pagination)"
    ),
    limit: int = Query(
        default=100, ge=1, le=100, description="Maximum number of tasks to return"
    ),
    task_controller: TaskController = Depends(Factory().get_task_controller),
) -> List[TaskResponse]:
    """
    Retrieve a list of all tasks.

    This endpoint returns a paginated list of tasks. You can optionally filter
    by completion status.

    Args:
        skip (int): Number of tasks to skip (for pagination)
        limit (int): Maximum number of tasks to return
        completed (Optional[bool]): Filter by completion status
        task_controller (TaskController): The task controller instance

    Returns:
        List[TaskResponse]: List of tasks matching the criteria
    """
    return await task_controller.get_all(skip=skip, limit=limit)


@task_router.get(
    "/{task_id}",
    summary="Get Task by ID",
    description="""
    Retrieve a specific task by its ID.
    
    This endpoint allows you to:
    * Get a single task by ID
    * View all task details
    
    The task ID must be a positive integer.
    """,
    tags=["Tasks"],
    status_code=status.HTTP_200_OK,
    response_description="Task retrieved successfully",
    response_model=TaskResponse,
    responses={
        404: {"model": NotFoundError, "description": "Task not found"},
        400: {"model": InvalidFormatError, "description": "Invalid format for Task id"},
        500: {"model": DatabaseError, "description": "Database error occured"},
    },
)
async def get_task(
    task_id: str = Path(..., description="The ID of the task to retrieve", example="1"),
    task_controller: TaskController = Depends(Factory().get_task_controller),
) -> TaskResponse:
    """
    Retrieve a specific task by its ID.

    Args:
        task_id (str): The ID of the task to retrieve
        task_controller (TaskController): The task controller instance

    Returns:
        TaskResponse: The requested task

    Raises:
        BadRequestException: If the task ID is not a valid number
        NotFoundException: If the task is not found
    """
    if not task_id.isdigit():
        raise BadRequestException("Expected number, but received string")
    task = await task_controller.get_by_id(id=int(task_id))
    return task


@task_router.put(
    "/{task_id}",
    summary="Update Task",
    description="""
    Update an existing task by its ID.
    
    This endpoint allows you to:
    * Update task title
    * Update task description
    * Update completion status
    
    The task ID must be a positive integer.
    Only provided fields will be updated.
    """,
    tags=["Tasks"],
    status_code=status.HTTP_200_OK,
    response_description="Task updated successfully",
    response_model=TaskResponse,
    responses={
        404: {"model": NotFoundError, "description": "Task not found"},
        400: {"model": InvalidFormatError, "description": "Invalid format for Task id"},
        500: {"model": DatabaseError, "description": "Database error occured"},
    },
)
async def update_task(
    task_id: str = Path(..., description="The ID of the task to update", example="1"),
    task_update: TaskUpdateRequest = Body(
        ...,
        description="Updated task data",
        example={
            "title": "Buy More Groceries",
            "description": "Updated shopping list",
            "completed": True,
        },
    ),
    task_controller: TaskController = Depends(Factory().get_task_controller),
) -> TaskResponse:
    """
    Update an existing task.

    Args:
        task_id (str): The ID of the task to update
        task_update (TaskUpdateRequest): The updated task data
        task_controller (TaskController): The task controller instance

    Returns:
        TaskResponse: The updated task

    Raises:
        BadRequestException: If the task ID is not a valid number
        NotFoundException: If the task is not found
        UnprocessableEntity: If no updates are provided
    """
    if not task_id.isdigit():
        raise BadRequestException("Expected number, but received string")
    task = await task_controller.update(
        id=int(task_id),
        attributes=task_update.model_dump(),
    )
    return task


@task_router.delete(
    "/{task_id}",
    summary="Delete Task",
    description="""
    Delete a task by its ID.
    
    This endpoint allows you to:
    * Permanently delete a task
    
    The task ID must be a positive integer.
    This operation cannot be undone.
    """,
    tags=["Tasks"],
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Task deleted successfully",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"model": NotFoundError, "description": "Task not found"},
        400: {"model": InvalidFormatError, "description": "Invalid format for Task id"},
        500: {"model": DatabaseError, "description": "Database error occured"},
    },
)
async def delete_task(
    task_id: Union[int, str] = Path(
        ..., description="The ID of the task to delete", example="1"
    ),
    task_controller: TaskController = Depends(Factory().get_task_controller),
):
    """
    Delete a task by its ID.

    Args:
        task_id (Union[int, str]): The ID of the task to delete
        task_controller (TaskController): The task controller instance

    Returns:
        None

    Raises:
        BadRequestException: If the task ID is not a valid number
        NotFoundException: If the task is not found
    """
    if not task_id.isdigit():
        raise BadRequestException("Expected number, but received string")
    return await task_controller.delete(id=int(task_id))
