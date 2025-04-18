FROM python:3.12

WORKDIR /backend

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

RUN poetry install --no-root

COPY . .

CMD alembic upgrade head && uvicorn src.main:app --host "0.0.0.0" --port 8080 --reload
