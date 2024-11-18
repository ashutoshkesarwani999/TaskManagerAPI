from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.config import config
from core.utils.logging import logger

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engines = {
    "writer": create_async_engine(
        config.POSTGRES_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    ),
    "reader": create_async_engine(
        config.POSTGRES_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    ),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        """
        select the Read or write engine based on the query type
        """
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


async def get_session():
    """
    Get the database session for the current request.
    """
    try:
        yield session
    finally:
        await session.close()


async def test_connection():
    """
    Test the database connection.
    """
    token = set_session_context("test-connection")
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}", exc_info=True)
        return False
    finally:
        reset_session_context(token)


Base = declarative_base()
