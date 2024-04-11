FROM python:3.10

WORKDIR /app
COPY . /app
CMD make setup

CMD poetry run python /app/semantic/backend/main.py
