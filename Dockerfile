FROM python:3.12

WORKDIR /backend

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

RUN poetry install --no-root

COPY . .

RUN chmod a+x ./build/*.sh

CMD [ "sh", "./build/app_entrypoint.sh" ]