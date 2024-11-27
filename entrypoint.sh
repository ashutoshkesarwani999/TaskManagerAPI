#!/bin/sh

DIR="alembic/versions"
if [ -d "$DIR" ]; then
    echo "Directory $DIR exists."
else:
    echo "Directory $DIR does not exist."
    mkdir -p "$DIR"
fi

poetry run alembic check
status=$?

if [ $status -eq 0  ]; then
    echo "NO changes detected"
else
    echo "Chagnes detected. Running alembic migration"
    poetry run alembic revision --autogenerate -m "Initial Migration"
    # Run Alembic migrations
    poetry run alembic upgrade head

# Start FastAPI server
poetry run python main.py