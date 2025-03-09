FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN apt update && apt upgrade
RUN apt install -y build-essential curl g++ gcc gettext git make libc-dev libffi-dev memcached pkg-config wget
RUN apt install -y apt-transport-https ca-certificates dirmngr software-properties-common
RUN apt install -y python3-dev python3-pip python3-virtualenv default-libmysqlclient-dev python3-psycopg2
RUN apt install -y nodejs npm
RUN npm install -g npm bower less recess

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
