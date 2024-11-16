FROM python:3.12-slim

WORKDIR .
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install
COPY . . 

ENV HOST=0.0.0.0
EXPOSE 8000

CMD ["python", "main.py"]