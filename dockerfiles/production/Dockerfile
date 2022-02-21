FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 fonts-liberation

WORKDIR /app

COPY requirements /app/requirements
RUN pip install -r requirements/production.txt

COPY . /app


