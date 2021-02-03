FROM python:3

RUN mkdir -p /srv/app
WORKDIR /srv/app

COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app .

CMD ["flask", "run", "--host=0.0.0.0"]
