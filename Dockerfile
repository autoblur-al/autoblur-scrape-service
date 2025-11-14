FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
