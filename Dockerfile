FROM python:3.11-slim

LABEL maintainer="karim"
LABEL description="FastAPI chat app"
LABEL version="1.0.0"

WORKDIR src/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic alembic
COPY alembic.ini alembic.ini

COPY ./app ./app

COPY README.md README.md
COPY LICENSE LICENSE

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

