FROM python:3.12.1-alpine3.19

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry update

COPY . .

CMD poetry run python3 run.py