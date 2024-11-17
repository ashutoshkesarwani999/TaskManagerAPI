import asyncio
import os
from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import core.database.transaction as transactional
from app.models.task import Base
from core.config import config

TEST_DATABASE_URL = config.POSTGRES_URL

# Override the config to use the test database
config.POSTGRES_URL = TEST_DATABASE_URL


# @pytest.fixture(scope="session")
# def event_loop(request) -> Generator:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(config.POSTGRES_URL)
    session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    # async with session() as s:
    #     async with async_engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.create_all)

    #     transactional.session = s
    #     yield s

    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     pass

    # await async_engine.dispose()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create and yield session
    session = session()
    try:
        yield session
    finally:
        await session.close()
        # Drop tables and cleanup
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await async_engine.dispose()
