# Introduction

A Task Manager API for managing tasks in a to-do list application. The API allows users to:

* Create Tasks
* Retrieve a list of all tasks
* Retrieve details of a specific task
* Update a task
* Delete a task

## Task Model


The `Task` class represents a task entity in the database. This model includes the following fields:

- **id**: The unique identifier of the task (Primary Key, Auto Increment).
- **title**: A required string field for the task's title (max length 255).
- **description**: An optional string field for the task's description (max length 255).
- **completed**: A boolean indicating whether the task is completed (default: `False`).
- **created_at**: The timestamp when the task was created (default: current time).


![diagram](/class_diag.png)
### Features

- Python 3.11+ support
- SQLAlchemy 2.0+ support
- Asynchoronous capabilities
- Database migrations using Alembic
- Testing suite
- Type checking using mypy
- Dockerized database
- Readily available CRUD operations
- Linting using pylint
- Formatting using black


### Installation Guide

You need following to run this project:

- Python 3.12
- Docker with Docker Compose
- makefile
- pytest

Once you have installed the required tools and cloned the repository, follow these steps to get the project up and running:

1. Copy the `.env.example` file to `.env` and update the values as needed.

2. Run the database and Redis containers:

    ```bash
    docker-compose up --build
    ```
    Note: On the latest Ubuntu, use the following command:

    ```bash
    docker compose up --build
    ```

    The server should now be running at `http://0.0.0.0:8000` and the API documentation should be available at `http://0.0.0.0:8000/docs`.

3. In a new terminal, run the tests (unit tests and BDD tests):

    ```bash
    make test
    ```

    Or, if you have `pytest` installed instead, you can run:

    ```bash
    pytest -vv -s --cache-clear ./
    ```

4. Other make targets with descriptions can be found in the [Makefile Config](#makefile-config).


### Directory Guide

The project is designed to be modular and scalable. There are 3 main directories in the project:

1. `core`: This directory contains the central part of this project. It contains most of the dependencies, database connections, configuration, middlewares etc. It also contains the base classes for the models, repositories, and controllers. The `core` directory is designed to be as minimal as possible and usually requires minimal attention.

2. `app`: This directory contains the actual application code. It contains the models, repositories, controllers, and schemas for the application. 

3. `api`: This directory contains the API layer of the application. It contains the API router, it is where you add the API endpoints.

4. `test`: This stores all the test cases unittest and the BDD test cases. Currently it uses the postgre db to execute the test cases.


### Makefile Config

This Makefile defines various commands for managing the development environment, database migrations, linting, testing, and formatting.

#### Targets:

- **install**: Install project dependencies using Poetry.
- **run**: Start the application by running `main.py` using Poetry.
- **migrate**: Apply database migrations using Alembic.
- **rollback**: Roll back the last database migration using Alembic.
- **reset-database**: Reset the database to its initial state (downgrade to base) using Alembic.
- **generate-migration**: Generate a new migration file using Alembic with an autogenerated message.
  
#### Code Quality and Formatting:
- **check**: Run `check-format` and `lint` to verify code quality and format.
- **check-format**: Check that the code is formatted correctly using `black` and `isort`.
- **lint**: Run `pylint` to check for linting errors in the `api`, `app`, and `core` directories.
- **format**: Automatically format the code using `black` and `isort`.

- **check-lockfile**: Ensure that the Poetry lock file is up-to-date with dependencies.
  
#### Testing:
- **test**: Run tests using `pytest`, clearing the cache and running with verbose output.
