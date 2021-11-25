FROM python:3

RUN mkdir -p /srv/test
WORKDIR /srv/test

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ .

COPY ./images/seed.sh /usr/local/bin/seed
COPY  ./images/migrate.sh /usr/local/bin/migrate
