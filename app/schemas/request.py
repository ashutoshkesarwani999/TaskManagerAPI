from typing import Optional

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class TaskCreateRequest(BaseModel):
    id: Annotated[int, Field(..., description="Task ID", examples=[1], gt=0)]
    title: Annotated[
        str,
        Field(
            ...,
            description="Title of the Task",
            examples=["Buy Groceries"],
            min_length=1,
        ),
    ]
    description: Optional[str] = Field(
        None, description="Describe the task", examples=["Milk, Eggs, Bread"]
    )
    completed: Optional[bool] = (
        Field(default=False, description="Task completion status", examples=[False]),
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: int) -> int:
        if v is None:
            raise ValueError("Task ID is required")
        if v <= 0:
            raise ValueError("Task ID must be a positive integer")
        return v

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("Title must not be empty")
        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError("Title cannot be empty or whitespace")
        return stripped_value


class TaskUpdateRequest(BaseModel):

    title: Optional[str] = Field(
        ..., description="Title of the Task", examples=["Buy Groceries"]
    )

    description: Optional[str] = Field(
        None, description="Describe the task", examples=["Milk, Eggs, Bread"]
    )
    completed: Optional[bool] = (
        Field(default=False, description="Task completion status", examples=[False]),
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("Title must not be empty")
        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError("Title cannot be empty or whitespace")
        return stripped_value
