# tests/repository/test_base_repo.py
import pytest
import pytest_asyncio
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from core.exceptions.base import DatabaseError, UnprocessableEntity
from core.repository.base import BaseRepo
from tests.factory.task import create_fake_task


@pytest_asyncio.fixture
async def test_repo(db_session: AsyncSession):
    return BaseRepo(Task, db_session)


@pytest.mark.asyncio
class TestBaseRepo:
    async def test_create_success(self, test_repo: BaseRepo[Task]):
        # Given
        test_data = create_fake_task()

        # When
        instance = await test_repo.create(test_data)

        # Then
        assert instance == test_data

    async def test_create_duplicate(self, test_repo: BaseRepo[Task]):
        # Given
        test_data = create_fake_task()
        await test_repo.create(test_data)

        # When/Then
        with pytest.raises(UnprocessableEntity) as error:
            await test_repo.create(test_data)

    async def test_get_all(self, test_repo: BaseRepo[Task]):
        test_data = [create_fake_task() for i in range(2)]
        for data in test_data:
            await test_repo.create(data)

        # When
        results = await test_repo.get_all()

        # Then
        assert len(results) == len(test_data)

    async def test_get_all_with_pagination(self, test_repo: BaseRepo[Task]):
        # Given
        test_data = [create_fake_task() for i in range(5)]
        for data in test_data:
            await test_repo.create(data)

        # When
        results = await test_repo.get_all(skip=1, limit=2)

        # Then
        assert len(results) == 2

    async def test_get_by_field(self, test_repo: BaseRepo[Task]):
        # Given
        test_data = create_fake_task()
        created = await test_repo.create(test_data)

        # When
        result = await test_repo.get_by_field(field="title", value=test_data["title"])

        # Then
        assert result.id == created.id

    async def test_get_by_field_not_found(self, test_repo: BaseRepo[Task]):
        # When
        result = await test_repo.get_by_field("title", "nonexistent")

        # Then
        assert result is None

    async def test_get_by_field_invalid_field(self, test_repo: BaseRepo[Task]):
        # When/Then
        with pytest.raises(ValueError, match="Field 'invalid' does not exist"):
            await test_repo.get_by_field(field="invalid", value="value")

    async def test_update_by_id(self, test_repo: BaseRepo[Task]):
        # Given
        test_task = create_fake_task()
        instance = await test_repo.create(test_task)

        # When
        await test_repo.update_by_id(
            id=instance.id,
            params={
                "title": test_task["title"],
                "description": "Milk, Eggs, Bread, Butter",
                "completed": False,
            },
        )
        await test_repo.refresh(instance)
        # Then
        updated = await test_repo.get_by_field("id", instance.id)
        assert updated.description == "Milk, Eggs, Bread, Butter"
        assert updated.title == test_task["title"]

    async def test_delete(self, test_repo: BaseRepo[Task]):
        # Given
        test_task = create_fake_task()
        instance = await test_repo.create(test_task)
        # When
        await test_repo.delete(instance)

        # Then
        result = await test_repo.get_by_field("id", instance.id)
        assert result is None

    async def test_delete_by_id(self, test_repo: BaseRepo[Task]):
        # Given
        test_task = create_fake_task()
        instance = await test_repo.create(test_task)

        # When
        await test_repo.delete_by_id(instance.id)

        # Then
        result = await test_repo.get_by_field(field="id", value=instance.id)
        assert result is None

    async def test_refresh(self, test_repo: BaseRepo[Task]):
        # Given
        test_task = create_fake_task()
        instance = await test_repo.create(test_task)

        # When - Update directly in DB
        await test_repo.update_by_id(instance.id, {"description": "updated"})
        await test_repo.refresh(instance)

        # Then
        assert instance.description == "updated"

    async def test_session_rollback_on_error(self, test_repo: BaseRepo[Task]):
        # Given
        test_data = {"title": None}

        # When/Then
        with pytest.raises(UnprocessableEntity):
            await test_repo.create(test_data)

        # Verify session is not usable
        test_task = create_fake_task()
        with pytest.raises(DatabaseError):
            instance = await test_repo.create(test_task)

    async def test_create_with_none_session(self):
        # Given
        repo = BaseRepo(Task, None)

        # When/Then
        with pytest.raises(ValueError, match="Session is not initialized"):
            await repo.create({"title": "test"})

    async def test_get_all_empty(self, test_repo: BaseRepo[Task]):
        # When
        results = await test_repo.get_all()

        # Then
        assert len(results) == 0

    async def test_update_by_id_nonexistent(self, test_repo: BaseRepo[Task]):
        # When
        test_task = create_fake_task(
            title="Buy Groceries", description="Test desc", completed=False
        )
        with pytest.raises(Exception, match="No record found with id 999"):
            await test_repo.update_by_id(999, test_task)

    async def test_delete_by_id_nonexistent(self, test_repo: BaseRepo[Task]):
        # When/Then - Should not raise
        with pytest.raises(Exception, match="No record found with id 999"):
            await test_repo.delete_by_id(999)
