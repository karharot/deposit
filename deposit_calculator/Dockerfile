FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    build-essential

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY .. /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
