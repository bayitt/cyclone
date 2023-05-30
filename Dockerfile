FROM python:3.10-slim-buster

RUN mkdir -p /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev python-dev build-essential gcc

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./cyclone /app/cyclone

EXPOSE 8000

CMD ["uvicorn", "cyclone.app:app", "--host", "0.0.0.0", "--port", "8000"]