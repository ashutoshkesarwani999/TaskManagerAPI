
.PHONY: install
install: 
	poetry install

.PHONY: run
run: start

.PHONY: start
start: 
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run python main.py

.PHONY: migrate
migrate: 
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run alembic upgrade head

.PHONY: rollback
rollback: 
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run alembic downgrade -1

.PHONY: reset-database
reset-database: 
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run alembic downgrade base

.PHONY: generate-migration 
generate-migration: 
	$(eval include .env) 
	$(eval export $(sh sed 's/=.*//' .env)) 

	@read -p "Enter migration message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"



# Check, lint and format targets
.PHONY: check
check: check-format lint

.PHONY: check-format
check-format: 
	poetry run black ./ --check
	poetry run isort ./ --profile black --check

.PHONY: lint
lint: 
	poetry run pylint ./api ./app ./core
 
.PHONY: format
format: 
	poetry run black ./
	poetry run isort ./ --profile black

.PHONY: check-lockfile
check-lockfile: 
	poetry lock --check

.PHONY: test
test: 
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run pytest -vv -s --cache-clear ./