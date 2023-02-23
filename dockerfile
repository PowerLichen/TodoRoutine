FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app/server

COPY ./Pipfile ./
COPY ./Pipfile.lock ./
RUN pipenv install --system

COPY . ./
