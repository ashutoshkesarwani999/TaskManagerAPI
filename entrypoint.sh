#!/bin/sh

poetry run alembic revision --autogenerate -m "Initial Migration"

# Run Alembic migrations
poetry run alembic upgrade head

# Start FastAPI server
poetry run python main.py