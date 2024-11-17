# Introduction

A Task Manager API for managing tasks in a to-do list application. The API allows users to:

* Create Tasks
* Retrieve a list of all tasks
* Retrieve details of a specific task
* Update a task
* Delete a task

## Task Model

* id : unique
* title: string
* description: string
* completed: boolean
* created_at: timestamp


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

- Python 3.11
- [Docker with Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

I use [asdf](https://asdf-vm.com/#/) to manage my python versions. You can use it too. However, it is only supported on Linux and macOS. For Windows, you can use something like pyenv.

Once you have installed the above and have cloned the repository, you can follow the following steps to get the project up and running:

1. Create a virtual environment using poetry:

```bash
poetry shell
```

2. Install the dependencies:

```bash
poetry install
```

3. Run the database and redis containers:

```bash
docker-compose up --build
```
Note: For latest Ubuntu 
```bash
docker compose up --builld
```

4. Copy the `.env.example` file to `.env` and update the values as per your needs.

5. Run the migrations:

```bash
make migrate
```

6. Run the server:

```bash
make run
```

The server should now be running on `http://localhost:8000` and the API documentation should be available at `http://localhost:8000/docs`.


