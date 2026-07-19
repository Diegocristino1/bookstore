FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000
