FROM python:3.10-slim-buster

LABEL maintainer="mohammades13851@gmail.com"

ENV PYTHONUNBUFFERED=1


WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./ .