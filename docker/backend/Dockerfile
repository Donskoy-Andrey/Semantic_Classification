FROM python:3.10

WORKDIR /app
COPY . /app
CMD make setup

CMD poetry run uvicorn /app/semantic/backend/main.py:app --host 0.0.0.0 --port 8000