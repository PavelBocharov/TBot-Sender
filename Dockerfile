FROM python:3.12-slim

ENV UVICORN_HOST="0.0.0.0"
ENV UVICORN_PORT="8080"

WORKDIR /opt/app

COPY ./src ./src
COPY ./Pipfile ./Pipfile
COPY ./main.py ./main.py
COPY ./telegram_worker.py ./telegram_worker.py

RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "uvicorn", "main:app"]

EXPOSE 8080