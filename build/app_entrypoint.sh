#!/bin/bash
poetry run sleep 2 #
poetry run alembic upgrade head #
poetry run python -c "from src.parse_to_db import parse_to_db; from src.config import settings; parse_to_db(settings.POSTGRES_URL.replace('asyncpg', 'psycopg'))"
poetry run gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind="0.0.0.0:8000" --access-logfile - --error-logfile - --log-level info
