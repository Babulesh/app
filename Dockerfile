FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi --no-root

COPY . .

CMD ["gunicorn", "hotel.wsgi:application",            \
     "--bind", "0.0.0.0:8000",                        \
     "--workers", "3",                                \
     "--threads", "2",                                \
     "--timeout", "60"]
