#!/bin/bash
poetry run sleep 2 #
poetry run alembic upgrade head #
poetry run python3 -m src.seeds.v1.create #
poetry run gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind="0.0.0.0:8000" --access-logfile - --error-logfile - --log-level info
