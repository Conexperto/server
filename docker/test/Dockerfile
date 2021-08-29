FROM python:3

RUN mkdir -p /srv/test
WORKDIR /srv/test

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ .
