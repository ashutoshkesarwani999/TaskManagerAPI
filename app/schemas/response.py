from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class TaskResponse(BaseModel):
    id: Annotated[int, Field(None, description="Task ID", examples=[1])]
    title: Annotated[
        str, Field(..., description="Title of the Task", examples=["Buy Groceries"])
    ]
    description: Optional[str] = Field(
        None, description="Describe the task", examples=["Milk, Eggs, Bread"]
    )
    completed: Optional[bool] = (
        Field(..., description="Task completion status", examples=[False]),
    )
    created_at: Annotated[
        datetime,
        Field(
            None,
            description="Timestamp when the task was created",
            examples=["2024-11-16T14:30:00"],
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status", examples=["healthy"])
    database_connected: bool = Field(
        ..., description="Database connection status", examples=[True]
    )
