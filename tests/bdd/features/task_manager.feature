Feature: Task Management

  # Health check for the API
  Scenario: Check if the Task Manager API is running
    Given a running Task Manager API
    Then the API should respond with a status code of 200

  # Creating a task
  Scenario: Create a new task
    When I create a new task
    Then the task should be created with status code 201

  # Retrieving tasks
  Scenario: Retrieve a list of all tasks
    When I retrieve the list of all tasks
    Then the response should contain a list of tasks with status code 200

  # Task existence with ID
  Scenario: A task exists
    Given a task exists
    When I retrieve the task
    Then the task details should be returned with status code 200

  # Updating a task
  Scenario: Update task with new description
    Given a task exists
    When I update the task to have description "Updated task description"
    Then the task should be updated with status code 200 and description "Updated task description"

  # Deleting a task
  Scenario: Delete a task
    Given a task exists 
    When I delete the task
    Then the task should be deleted with status code 204

  # Retrieving a non-existent task
  Scenario: Retrieve a non-existent task
    When I retrieve the task with ID "9998763"
    Then the response should be no task "9998763" found with status code 404

  # Creating duplicate tasks
  Scenario: Try to create another task with the same title and description
    When I try to create another task with title "Task title" and description "Task description"
    Then the response should be Unique constraint violation
