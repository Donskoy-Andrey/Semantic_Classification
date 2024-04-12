FROM python:3.10

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY ../../ /app

RUN python -m pip install poetry

RUN poetry install

EXPOSE 8000

CMD ["poetry", "shell"]

CMD ["poetry", "run", "uvicorn", "semantic.backend.main:app", "--host", "localhost", "--reload", "--port", "8000"]
