FROM python:3.9.6-alpine

WORKDIR /app

COPY ./requirements.txt ./

RUN apk update && apk add --no-cache --virtual python3-dev gcc libc-dev libffi-dev postgresql-dev build-base alpine-sdk

RUN pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir -r requirements.txt

RUN pip uninstall PyJWT -y
RUN pip install PyJWT

COPY ./src ./src
EXPOSE 8000

# CMD [ "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
CMD [ "gunicorn", "--bind", ":8000", "asgi:channel_layer", "--worker-class", "uvicorn_worker.Worker", "--reload" ]
