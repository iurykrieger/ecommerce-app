FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src src

ENTRYPOINT flask run -h 0.0.0.0