import pytest
from fastapi.testclient import TestClient
from core.server import app
from pytest_bdd import scenarios, given, when, then, parsers

client = TestClient(app)

scenarios("features/task_manager.feature")

@pytest.fixture  
def task_data()-> dict:  
    return {}

@pytest.fixture  
def task_data_list()-> list:  
    return []

@given("a running Task Manager API")
def running_task_manager_api(task_data):
    response = client.get("/v1/health/")
    assert response.status_code == 200
    print(f"API health check passed: {response.status_code}")


@when('I create a new task with title Buy groceries and description Milk, Eggs, Bread')
def create_task(task_data):
    print("Hello")
    title= "Buy groceries"
    description = "Milk, Eggs, Bread"
    response = client.post("/v1/tasks/", json={
    "id": 1,
    "title": "Buy Groceries",
    "description": "Milk, Eggs, Bread",
    "completed": False,
    "created_at": "2024-11-16T14:30:00"
  })
    assert response.status_code == 201
    task_data.update(response.json())


@then("the task should be created with status code 201")
def verify_task_created(task_data):
    assert task_data["title"] == "Buy Groceries"
    assert task_data["description"] == "Milk, Eggs, Bread"
    assert task_data["id"] is not None  # Ensure task has an ID

@when("I retrieve the list of all tasks")
def retrieve_all_tasks(task_data_list):
    response = client.get("/v1/tasks/")
    assert response.status_code == 200
    print("task data is ",task_data_list)

    task_data_list.append(response.json())
    print("task data is ",task_data_list)


@then("the response should contain a list of tasks with status code 200")
def verify_all_tasks(task_data_list):
    print(task_data_list)
    assert isinstance(task_data_list, list)
    assert len(task_data_list) > 0  


@given(parsers.parse('a task exists with ID "{task_id:d}"'))
def task_exists(task_id):
    response = client.post("/v1/tasks/", json={
    "id": 1,
    "title": "Buy Groceries",
    "description": "Milk, Eggs, Bread",
    "completed": False,
    "created_at": "2024-11-16T14:30:00"
  })
    assert response.status_code == 201


@when(parsers.parse('I retrieve the task with ID "{task_id:d}"'))
def retrieve_task(task_data, task_id):
    response = client.get(f"/v1/tasks/{task_id}")
    assert response.status_code == 200
    task_data.update(response.json())


@then(parsers.parse('the task details should be returned with status code 200 and task ID "{task_id:d}"'))
def verify_task_details(task_data,task_id):
    assert task_data["id"] == int(task_id)
    assert task_data["title"] == "Buy Groceries"
    assert task_data["description"] == "Milk, Eggs, Bread"


@given(parsers.parse('a task exists with ID "{task_id:d}"'))
def task_exists(task_id):
    response = client.post("/v1/tasks/", json={
    "id": 1,
    "title": "Buy Groceries",
    "description": "Milk, Eggs, Bread",
    "completed": False,
    "created_at": "2024-11-16T14:30:00"
  })
    assert response.status_code == 201


@when(parsers.parse("I update the task with ID {task_id} to have description \"{new_description}\""))
def update_task(task_data, task_id, new_description):
    response = client.put(f"/v1/tasks/{task_id}", json={"description": new_description})
    assert response.status_code == 200
    task_data.update(response.json())


@then("the task should be updated with status code 200")
def verify_task_updated(task_data):
    assert task_data["title"] == "Buy Groceries"  # Ensure title was updated
    assert task_data["description"] == "Milk, Eggs, Bread, Butter"


@given(parsers.parse('a task exists with ID "{task_id:d}"'))
def task_exists(task_id):
    response = client.post("/v1/tasks/", json={
    "id": 1,
    "title": "Buy Groceries",
    "description": "Milk, Eggs, Bread",
    "completed": False,
    "created_at": "2024-11-16T14:30:00"
  })
    assert response.status_code == 201


@when(parsers.parse("I delete the task with ID {task_id}"))
def delete_task(task_id):
    response = client.delete(f"/v1/tasks/{task_id}")
    assert response.status_code == 204


@then(parsers.parse("the task with ID {task_id} should be deleted with status code 204"))
def verify_task_deleted(task_data,task_id):
    response = client.get(f"/v1/tasks/{task_id}")
    print("respones",response.json())
    assert response.status_code == 404


@when(parsers.parse("I retrieve the task with ID {task_id}"))
def retrieve_nonexistent_task(task_data, task_id):
    response = client.get(f"/v1/tasks/{task_id}")
    assert response.status_code == 404
    task_data.update(response.json())


# Then: Verify non-existent task retrieval
@then("the response should be no task found with status code 404")
def verify_nonexistent_task(task_data):
    assert task_data["detail"] == "Task not found"



# Scenario: Creating a task with a duplicate title
@given(parsers.parse('a task exists with title "{title}" and description "{description}"'))
def create_existing_task(title, description):
    response = client.post(
        "/v1/tasks/",
        json={"title": title, "description": description, "completed": False},
    )
    assert response.status_code == 201


@when(parsers.parse('I try to create another task with title "{title}" and description "{description}"'))
def create_duplicate_task(title, description, task_data):
    response = client.post(
        "/v1/tasks/",
        json={"title": title, "description": description, "completed": False},
    )
    task_data.update(response.json())
    assert response.status_code == 400


@then(parsers.parse('the response should have status code 400 and detail "{error_message}"'))
def verify_duplicate_task_error(task_data, error_message):
    assert task_data["detail"] == error_message


# Scenario: Marking a task as complete
@given(parsers.parse('a task exists with ID "{task_id:d}" and completed status {completed_status}'))
def task_with_completed_status(task_id, completed_status):
    response = client.post(
        "/v1/tasks/",
        json={
            "id": task_id,
            "title": "Buy Groceries",
            "description": "Milk, Eggs, Bread",
            "completed": completed_status == "True",
        },
    )
    assert response.status_code == 201


@when(parsers.parse('I update the task with ID "{task_id}" to mark it as complete'))
def mark_task_complete(task_data, task_id):
    response = client.put(f"/v1/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    task_data.update(response.json())


@then(parsers.parse('the task should be updated with status code 200 and completed status {completed_status}'))
def verify_task_marked_complete(task_data, completed_status):
    assert task_data["completed"] == (completed_status == "True")


# Scenario: Creating a task with an empty title
@when('I try to create a new task with an empty title and description "Description for empty title"')
def create_task_with_empty_title(task_data):
    response = client.post(
        "/v1/tasks/",
        json={"title": "", "description": "Description for empty title"},
    )
    task_data.update(response.json())
    assert response.status_code == 422


@then(parsers.parse('the response should have status code {status_code} and detail "{error_message}"'))
def verify_task_creation_error(task_data, status_code, error_message):
    assert task_data["detail"] == error_message

# Scenario: Retrieving tasks when no tasks exist
@given("no tasks exist")
def clear_all_tasks():
    response = client.delete("/v1/tasks/")
    assert response.status_code in (200, 204)


@when("I retrieve the list of all tasks")
def retrieve_all_tasks(task_data_list):
    response = client.get("/v1/tasks/")
    assert response.status_code == 200
    task_data_list.append(response.json())


@then("the response should contain an empty list with status code 200")
def verify_no_tasks_exist(task_data_list):
    assert len(task_data_list[0]) == 0