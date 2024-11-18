from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from core.repository.base import BaseRepo


class TaskRepository(BaseRepo[Task]):
    """
    Task repository provides all the database operations for the Task model.
    """

    def __init__(self, db_session: AsyncSession):
        super().__init__(model=Task, db_session=db_session)
