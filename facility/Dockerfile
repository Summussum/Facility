

FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pwd
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ls

COPY . .
WORKDIR /facility
