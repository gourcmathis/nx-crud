FROM python:3.9-buster

RUN mkdir app
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:/.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .