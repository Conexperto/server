FROM node:15-alpine

WORKDIR /srv/test

RUN yarn global add jest

COPY ./test/package.json ./
RUN yarn install 

COPY ./test .

