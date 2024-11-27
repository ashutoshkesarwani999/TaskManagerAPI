from functools import partial

from fastapi import Depends

from app.controllers.task import TaskController
from app.models.task import Task
from app.repository.task import TaskRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    task_repository = partial(TaskRepository, Task)

    def get_task_controller(self, db_session=Depends(get_session)):
        return TaskController(task_repository=TaskRepository(db_session))
