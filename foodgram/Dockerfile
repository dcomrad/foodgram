FROM python:3.7-slim

COPY ../data .

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
