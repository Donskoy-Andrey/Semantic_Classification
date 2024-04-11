FROM python:3.10

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY ../../ /app

CMD ["make", "setup"]

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.semantic.backend.main:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]
