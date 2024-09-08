FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN apt update && apt install -y python3-dev wget git gcc make g++ libc-dev libffi-dev build-essential default-libmysqlclient-dev pkg-config python3-psycopg2 memcached gettext nodejs npm
RUN npm install -g bower less recess

RUN pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir -r requirements.txt

RUN pip uninstall PyJWT -y
RUN pip install PyJWT

COPY ./src ./src
RUN mkdir -p ./src/logs
RUN mkdir -p ./src/media

EXPOSE 8000

# CMD [ "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
# CMD [ "gunicorn", "--bind", ":8000", "asgi:channel_layer", "--worker-class", "uvicorn_worker.Worker", "--reload" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
