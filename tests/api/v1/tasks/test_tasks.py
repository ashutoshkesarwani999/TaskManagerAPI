import pytest
from httpx import AsyncClient

from tests.factory.task import create_fake_task


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, db_session) -> None:
    """Test task creation."""

    fake_task = create_fake_task()
    response = await client.post("/v1/tasks/", json=fake_task)
    assert response.status_code == 201
    assert response.json()["title"] == fake_task["title"]
    assert response.json()["description"] == fake_task["description"]
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_create_task_with_invalid_title(client: AsyncClient, db_session) -> None:
    """Test task creation with invalid title."""

    fake_task = create_fake_task()
    fake_task["title"] = ""

    response = await client.post("/v1/tasks/", json=fake_task)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_create_task_with_invalid_description(
    client: AsyncClient, db_session
) -> None:
    """Test task creation with invalid description."""

    fake_task = create_fake_task()
    fake_task["description"] = ""

    response = await client.post("/v1/tasks/", json=fake_task)
    assert response.status_code == 201
    assert response.json()["description"] is not None


@pytest.mark.asyncio
async def test_get_all_tasks(client: AsyncClient, db_session) -> None:
    """Test get all tasks."""

    await client.post("/v1/tasks/", json=create_fake_task())
    await client.post("/v1/tasks/", json=create_fake_task())
    await client.post("/v1/tasks/", json=create_fake_task())

    response = await client.get("/v1/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient, db_session) -> None:
    """Test get task by id."""

    task = await client.post("/v1/tasks/", json=create_fake_task())
    task_id = task.json()["id"]

    response = await client.get(f"/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(client: AsyncClient, db_session) -> None:
    """Test get task by id not found."""

    response = await client.get("/v1/tasks/1")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, db_session) -> None:
    """Test update task."""

    task = await client.post("/v1/tasks/", json=create_fake_task())
    task_id = task.json()["id"]

    fake_task = create_fake_task()
    fake_task["title"] = "Updated title"
    fake_task["description"] = "Updated description"

    response = await client.put(f"/v1/tasks/{task_id}", json=fake_task)
    assert response.status_code == 200
    assert response.json()["title"] == fake_task["title"]
    assert response.json()["description"] == fake_task["description"]
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_update_task_not_found(client: AsyncClient, db_session) -> None:
    """Test update task not found."""

    fake_task = create_fake_task()

    response = await client.put("/v1/tasks/1", json=fake_task)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, db_session) -> None:
    """Test delete task."""

    task = await client.post("/v1/tasks/", json=create_fake_task())
    task_id = task.json()["id"]

    response = await client.delete(f"/v1/tasks/{task_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_task_not_found(client: AsyncClient, db_session) -> None:
    """Test delete task not found."""

    response = await client.delete("/v1/tasks/1")
    assert response.status_code == 404
