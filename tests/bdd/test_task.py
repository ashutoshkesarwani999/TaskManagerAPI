import pytest
import requests
import json
from sqlalchemy.orm import Session
from core.database.session import get_session
from pytest_bdd import scenarios, given, when, then, parsers
from app.models.task import Task

# Replace with your actual API base URL
BASE_URL = "http://127.0.0.1:8000"

scenarios("features/task_manager.feature")

from tests.factory.task import create_fake_task


def custom_serializer(obj):
    if isinstance(obj, bool):
        return "true" if obj else "false"
    return obj


@pytest.fixture(scope="function")
def clear_db():
    db: Session = next(get_session())  # Assuming `get_db` provides the database session
    try:
        db.query(Task).delete()
        db.commit()
        yield db
    finally:
        db.rollback()


@pytest.fixture(scope="function")
def task_data() -> dict:
    return {}


@pytest.fixture(scope="function")
def task_data_list() -> list:
    return []


@given("a running Task Manager API")
def running_task_manager_api(task_data):
    response = requests.get(f"{BASE_URL}/v1/health/")
    assert response.status_code == 200
    task_data.update(response.json())


@then("the API should respond with a status code of 200")
def verify_healthy(task_data):
    assert task_data["status"] == "healthy"
    assert task_data["database_connected"] == True


@when("I create a new task")
def create_task(task_data):
    fake_task = create_fake_task()
    response = requests.post(f"{BASE_URL}/v1/tasks/", json=fake_task)
    assert response.status_code == 201
    task_data.update(response.json())


@then("the task should be created with status code 201")
def verify_task_created(task_data):
    assert task_data["id"] is not None
    assert isinstance(task_data["title"], str)
    assert isinstance(task_data["description"], str)


@when("I retrieve the list of all tasks")
def retrieve_all_tasks(task_data_list):
    response = requests.get(f"{BASE_URL}/v1/tasks/")
    assert response.status_code == 200
    task_data_list.append(response.json())


@then("the response should contain a list of tasks with status code 200")
def verify_all_tasks(task_data_list):
    assert isinstance(task_data_list[0], list)
    assert len(task_data_list[0]) > 0


@given(parsers.parse("a task exists"))
def task_exists(task_data):
    fake_task = create_fake_task()
    response = requests.post(f"{BASE_URL}/v1/tasks/", json=fake_task)
    task_data.update(response.json())
    assert response.status_code == 201


@when(parsers.parse("I retrieve the task"))
def retrieve_task(task_data):
    response = requests.get(f"{BASE_URL}/v1/tasks/{task_data["id"]}")
    task_data = {}
    assert response.status_code == 200
    task_data.update(response.json())


@then(parsers.parse("the task details should be returned with status code 200"))
def verify_task_details(task_data):
    assert isinstance(task_data["title"], str)
    assert isinstance(task_data["description"], str)


@when(parsers.parse('I update the task to have description "{new_description}"'))
def update_task(task_data, new_description):
    id = task_data["id"]
    del task_data["id"]
    del task_data["created_at"]
    task_data["description"] = new_description
    task_data["completed"] = str(task_data["completed"]).lower()
    response = requests.put(f"{BASE_URL}/v1/tasks/{id}", json=task_data)
    assert response.status_code == 200
    task_data.update(response.json())


@then(
    parsers.parse(
        'the task should be updated with status code 200 and description "{description}"'
    )
)
def verify_task_updated(task_data, description):
    assert isinstance(task_data["title"], str)
    assert task_data["description"] == description


@when(parsers.parse("I delete the task"))
def delete_task(task_data):
    response = requests.delete(f"{BASE_URL}/v1/tasks/{task_data["id"]}")
    assert response.status_code == 204


@then(parsers.parse("the task should be deleted with status code 204"))
def verify_task_deleted(task_data):
    response = requests.get(f"{BASE_URL}/v1/tasks/{task_data['id']}")
    assert response.status_code == 404


@when(parsers.parse('I retrieve the task with ID "{task_id}"'))
def retrieve_nonexistent_task(task_data, task_id):
    response = requests.get(f"{BASE_URL}/v1/tasks/{task_id}")
    assert response.status_code == 404
    task_data.update(response.json())


@then(
    parsers.parse(
        'the response should be no task "{task_id}" found with status code 404'
    )
)
def verify_nonexistent_task(task_data):
    assert task_data["detail"] == "Tasks with id: 9998763 does not exist"


# Example of using create_fake_task for duplicate tasks
@when(
    parsers.parse(
        'I try to create another task with title "{title}" and description "{description}"'
    )
)
def create_duplicate_task(title, description, task_data):
    fake_task = create_fake_task(title=title, description=description)
    response = requests.post(f"{BASE_URL}/v1/tasks/", json=fake_task)
    response = requests.post(f"{BASE_URL}/v1/tasks/", json=fake_task)
    task_data.update(response.json())
    assert response.status_code == 422


@then("the response should be Unique constraint violation")
def verify_duplicate_task(task_data):
    assert task_data["detail"] == "Unique constraint violation"
