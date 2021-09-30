FROM python:3.7-slim
ARG REQUIREMENTS_FILE=base.txt

WORKDIR /app
COPY requirements/${REQUIREMENTS_FILE} /app/

RUN pip install -r ${REQUIREMENTS_FILE}

