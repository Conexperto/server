FROM python:3

RUN mkdir /srv/app
WORKDIR /srv/app

COPY ./app/requirements.txt .
RUN pip3 install -r requirements.txt 

COPY ./app .

CMD ["flask", "run", "--host=0.0.0.0"]
