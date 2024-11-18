import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.task import Base
from core.config import config

TEST_DATABASE_URL = config.POSTGRES_URL

# Override the config to use the test database
config.POSTGRES_URL = TEST_DATABASE_URL


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(config.POSTGRES_URL)
    session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create and yield session
    session = session()
    try:
        yield session
    finally:
        await session.close()
        # # Drop tables and cleanup
        # async with async_engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
        await async_engine.dispose()
