from app.models.task import Task
from app.repository.task import TaskRepository
from core.controller.base import BaseController


class TaskController(BaseController[Task]):
    """Task Controller for managing task-related operations in the application."""

    def __init__(self, task_repository: TaskRepository):
        """Initialize the TaskController with necessary dependencies.
        Args:
            task_repository (TaskRepository): Repository instance for handling
                task-related database operations. Must implement BaseRepository
                interface.
        """
        super().__init__(model=Task, repository=task_repository)
        self.task_repository = task_repository
