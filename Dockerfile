FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей (libpq-dev для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей (важно: сначала копируем только эти файлы)
COPY pyproject.toml poetry.lock ./

# Установка Poetry и зависимостей
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копирование исходного кода
COPY . .

# Запуск Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
