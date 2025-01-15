FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /90_north

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt /90_north/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /90_north/


