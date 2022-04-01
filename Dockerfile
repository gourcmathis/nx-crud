FROM python:3.9-buster

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:/.

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ .