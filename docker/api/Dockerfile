FROM python:3

RUN mkdir -p /srv/app
WORKDIR /srv/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ .

COPY ./scripts/seed.sh /usr/local/bin/seed
COPY  ./scripts/migrate.sh /usr/local/bin/migrate


CMD ["flask", "run", "--host=0.0.0.0"]
