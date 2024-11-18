from app.controllers.task import TaskController
from app.models.task import Task
from app.repository.task import TaskRepository


class ControllerOverrides:
    def __init__(self, db_session):
        self.db_session = db_session

    def task_controller(self):
        return TaskController(TaskRepository(model=Task, session=self.db_session))
