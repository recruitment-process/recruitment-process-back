FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

RUN pip3 install drf-extra-fields==3.7.0

RUN apt-get update && apt-get install -y nano

COPY crm_backend/ .

CMD ["gunicorn", "crm_backend.wsgi:application", "--bind", "0:8000", "--reload"]
