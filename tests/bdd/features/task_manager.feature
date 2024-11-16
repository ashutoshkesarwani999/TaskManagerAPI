Feature: Task Manager API

  As a user
  I want to manage my tasks
  So that I can organize my work efficiently

  Scenario: Creating a new task
    Given a running Task Manager API
    When I create a new task with title "Buy groceries" and description "Milk, Eggs, Bread"
    Then the task should be created with status code 201

  Scenario: Retrieving all tasks
    Given a running Task Manager API
    When I retrieve the list of all tasks
    Then the response should contain a list of tasks with status code 200

  Scenario: Retrieving a specific task
    Given a running Task Manager API
    And a task exists with ID 1
    When I retrieve the task with ID 1
    Then the task details should be returned with status code 200

  Scenario: Updating a task
    Given a running Task Manager API
    And a task exists with ID 1
    When I update the task with ID 1 to have title "Clean house"
    Then the task should be updated with status code 200

  Scenario: Deleting a task
    Given a running Task Manager API
    And a task exists with ID 1
    When I delete the task with ID 1
    Then the task should be deleted with status code 204
