Feature: Task Manager API

  As a user
  I want to manage my tasks
  So that I can organize my work efficiently

  Scenario: Creating a new task
    Given a running Task Manager API
    When I create a new task with title Buy groceries and description Milk, Eggs, Bread
    Then the task should be created with status code 201

  Scenario: Retrieving all tasks
    Given a running Task Manager API
    When I retrieve the list of all tasks
    Then the response should contain a list of tasks with status code 200

  Scenario: Retrieving a specific task
    Given a running Task Manager API
    And a task exists with ID "1"
    When I retrieve the task with ID "1"
    Then the task details should be returned with status code 200 and task ID "1"

  Scenario: Updating a task
    Given a running Task Manager API
    And a task exists with ID "1"
    When I update the task with ID "1" to have description "Milk, Eggs, Bread, Butter"
    Then the task should be updated with status code 200

  Scenario: Deleting a task
    Given a running Task Manager API
    And a task exists with ID "1"
    When I delete the task with ID "1"
    Then the task with ID "1" should be deleted with status code 204

  Scenario: Fetching non existent task
    Given a running Task Manager API
    When I retrieve the task with ID "12394"
    Then the response should be no task found with status code 404
  
  Scenario: Creating a task with a duplicate title
    Given a running Task Manager API
    And a task exists with title "Buy groceries" and description "Milk, Eggs, Bread"
    When I try to create another task with title "Buy groceries" and description "Different description"
    Then the response should have status code 400 and detail "Task with this title already exists"

  Scenario: Updating a task to mark it as complete
    Given a running Task Manager API
    And a task exists with ID "1" and completed status False
    When I update the task with ID "1" to mark it as complete
    Then the task should be updated with status code 200 and completed status True

  Scenario: Creating a task with an empty title
    Given a running Task Manager API
    When I try to create a new task with an empty title and description "Description for empty title"
    Then the response should have status code 422 and detail "Title cannot be empty"

  # Scenario: Creating a task with an invalid date format
  #   Given a running Task Manager API
  #   When I try to create a new task with title "Invalid date task" and an invalid created_at date "2024-11-32T14:30:00"
  #   Then the response should have status code 422 and detail "Invalid date format"

  Scenario: Retrieving tasks when no tasks exist
    Given a running Task Manager API
    And no tasks exist
    When I retrieve the list of all tasks
    Then the response should contain an empty list with status code 200