FROM 3.10-slim-buster

RUN mkdir -p /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./cyclone /app/cyclone

CMD ["uvicorn", "cyclone.app:app", "--host", "0.0.0.0", "--port", "8000"]