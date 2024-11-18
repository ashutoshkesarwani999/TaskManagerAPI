from sqlalchemy import BigInteger, Boolean, Column, DateTime, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

from core.database import Base


class Base(DeclarativeBase):
    pass


class Task(AsyncAttrs, Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(
        String(255),
        nullable=False,
    )
    description = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def __eq__(self, other):
        if isinstance(other, dict):
            return (
                self.title == other.get("title")
                and self.description == other.get("description")
                and self.completed == other.get("completed")
            )
        return super().__eq__(other)
