from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone

from typing import Optional
from typing_extensions import Annotated


class TaskResponse(BaseModel):
    id: Annotated[int, Field(None, description="Task ID", examples=[1])]
    title: Annotated[
        str, Field(None, description="Title of the Task", examples=["Buy Groceries"])
    ]
    description: Optional[str] = Field(
        None, description="Describe the task", examples=["Milk, Eggs, Bread"]
    )

    completed: Annotated[
        bool,
        Field(default=False, description="Task completion status", examples=[False]),
    ]
    created_at: Annotated[
        datetime,
        Field(
            None,
            description="Timestamp when the task was created",
            examples=["2024-11-16T14:30:00"],
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


sampleListTaskResponse = {
    200: [
        {
            "id": 1,
            "title": "Buy Groceries",
            "description": "Milk, Eggs, Bread",
            "completed": False,
            "created_at": "2024-11-16T14:30:00",
        },
        {
            "id": 2,
            "title": "Clean House",
            "description": "Tidy up the entire house",
            "completed": False,
            "created_at": "2024-11-15T09:00:00",
        },
    ]
}

sampleTaskResponse = {
    200: {
        "id": 1,
        "title": "Buy Groceries",
        "description": "Milk, Eggs, Bread",
        "completed": False,
        "created_at": "2024-11-16T14:30:00",
    },
    404: {
        "description": "Task not found",
        "content": {"application/json": {"example": {"detail": "Task not found"}}},
    },
}
