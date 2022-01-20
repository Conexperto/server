<p align="center">
  <a href="http://nestjs.com/" target="blank"><img src="https://nestjs.com/img/logo_text.svg" width="320" alt="Nest Logo" /></a>
</p>

[circleci-image]: https://img.shields.io/circleci/build/github/nestjs/nest/master?token=abc123def456
[circleci-url]: https://circleci.com/gh/nestjs/nest

  <p align="center">A progressive <a href="http://nodejs.org" target="_blank">Node.js</a> framework for building efficient and scalable server-side applications.</p>
    <p align="center">
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/v/@nestjs/core.svg" alt="NPM Version" /></a>
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/l/@nestjs/core.svg" alt="Package License" /></a>
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/dm/@nestjs/common.svg" alt="NPM Downloads" /></a>
<a href="https://circleci.com/gh/nestjs/nest" target="_blank"><img src="https://img.shields.io/circleci/build/github/nestjs/nest/master" alt="CircleCI" /></a>
<a href="https://coveralls.io/github/nestjs/nest?branch=master" target="_blank"><img src="https://coveralls.io/repos/github/nestjs/nest/badge.svg?branch=master#9" alt="Coverage" /></a>
<a href="https://discord.gg/G7Qnnhy" target="_blank"><img src="https://img.shields.io/badge/discord-online-brightgreen.svg" alt="Discord"/></a>
<a href="https://opencollective.com/nest#backer" target="_blank"><img src="https://opencollective.com/nest/backers/badge.svg" alt="Backers on Open Collective" /></a>
<a href="https://opencollective.com/nest#sponsor" target="_blank"><img src="https://opencollective.com/nest/sponsors/badge.svg" alt="Sponsors on Open Collective" /></a>
  <a href="https://paypal.me/kamilmysliwiec" target="_blank"><img src="https://img.shields.io/badge/Donate-PayPal-ff3f59.svg"/></a>
    <a href="https://opencollective.com/nest#sponsor"  target="_blank"><img src="https://img.shields.io/badge/Support%20us-Open%20Collective-41B883.svg" alt="Support us"></a>
  <a href="https://twitter.com/nestframework" target="_blank"><img src="https://img.shields.io/twitter/follow/nestframework.svg?style=social&label=Follow"></a>
</p>
  <!--[![Backers on Open Collective](https://opencollective.com/nest/backers/badge.svg)](https://opencollective.com/nest#backer)
  [![Sponsors on Open Collective](https://opencollective.com/nest/sponsors/badge.svg)](https://opencollective.com/nest#sponsor)-->

## Description

[Nest](https://github.com/nestjs/nest) framework TypeScript starter repository.

## Installation

```bash
$ npm install
```

## Running the app

```bash
# development
$ npm run start

# watch mode
$ npm run start:dev

# production mode
$ npm run start:prod
```

## Test

```bash
# unit tests
$ npm run test

# e2e tests
$ npm run test:e2e

# test coverage
$ npm run test:cov
```

## Support

Nest is an MIT-licensed open source project. It can grow thanks to the sponsors and support by the amazing backers. If you'd like to join them, please [read more here](https://docs.nestjs.com/support).

## Stay in touch

- Author - [Kamil Myśliwiec](https://kamilmysliwiec.com)
- Website - [https://nestjs.com](https://nestjs.com/)
- Twitter - [@nestframework](https://twitter.com/nestframework)

## License

Nest is [MIT licensed](LICENSE).
=======
Conexperto Server
======

Conexperto, aims to be a social network to learn and grow. We believe that people learn best from other people, it was like that for a long time and this is how we actually learn from our environment.

This repository houses the code for all operation of the Backend in Conexperto.

## Getting Started 🚀

### Prerequisities

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)


### Instructions 🧐

Clone the repository and move to the project directory.
```sh
git clone git@gitlab.com:conexperto/server.git
```

Run build container.
```sh
docker-compose build
```

Run start container api.
```sh
docker-compose up api
```

Initialize migration of database.
```sh
docker-compose exec api db upgrade
```
if alterations are made in the api `src/models`, an update is necessary run this script.
```sh
docker-compose exec api db migrate
```

then visit <http://localhost:5000/api/v1/>

## Seeds 🥜
```
docker-compose exec api seed <seed> <up|down>
```
e.g.
```
docker-compose exec api seed user up
```
See folder `src/seeds` for more options.

## Testing 🔨
```
docker-compose run --rm test bash
```
For start container test.

Inside container.
```
pytest .
```
For exec all testing.

## Environment ⛺

### Environment for api.
In file `docker/api/api.conf` be all variables environment to api.
* `FLASK_RUN_PORT` 			- Set port for flask app.
* `FLASK_ENV`     			- Set env, 'production' or 'development'.
* `FLASK_DEBUG`   			- Set debug, enabled flask debug.
* `TESTING` 		  		- Set testing, enabled flask testing.
* `DATABASE_URL` 			- Set URL for connected to database.
* `FIREBASE_ADMIN_SDK_FILE` - Set path for sdk credentials admin.
* `FIREBASE_WEB_SDK_FILE`		- Set path for sdk credentials web.
* `FIREBASE_AUTH_EMULATOR_ADMIN_HOST` 	- Set host for emulator firebase admin.
* `FIREBASE_AUTH_EMULATOR_WEB_HOST`	- Set host for emulator firebase web.

### Environment for db
In file `docker/db/db.conf` be all variables envionment to db.
* `POSTGRES_MULTIPLE_DATABASES` 		- Set name database separate by command(,).
* `POSTGRES_PORT` 				- Set port, default `5432`.
* `POSTGRES_USER`				- Set user, default `owner`.
* `POSTGRES_PASSWORD`   			- Set password, defaullt `token.01`.

### Environment for test.
In file `docker/test/test.conf` be all variables environment to test.
* `FLASK_RUN_PORT` 			- Set port for flask app.
* `FLASK_ENV`     			- Set env, 'production' or 'development'.
* `FLASK_DEBUG`   			- Set debug, enabled flask debug.
* `TESTING` 				- Set testing, enabled flask testing.
* `DATABASE_URL` 			- Set URL for connected to database.
* `FIREBASE_ADMIN_SDK_FILE` - Set path for sdk credentials admin.
* `FIREBASE_WEB_SDK_FILE`		- Set path for sdk credentials web.
* `FIREBASE_AUTH_EMULATOR_ADMIN_HOST` 	- Set host for emulator firebase admin.
* `FIREBASE_AUTH_EMULATOR_WEB_HOST`	- Set host for emulator firebase web.
* `FIREBASE_API_KEY_ADMIN` 		- Set api key for authentication testing admin.
* `FIREBASE_API_KEY_WEB` 		- Set api key for authentication testing web.

## Folder Structure 📁
	.
	├── docker/ 					# resource for docker-compose
	|	├── api/				# container api
	|	|	├── Dockerfile 			# Contains all the comands for make image of container api.
	|	|	└── api.conf 			# environment variables for this container.
	| ├── db/					# container db
	|	|	├── pg-init-scripts/
	|	|	|	└── create-multiple-postgresql-database.sh # script for handle multiple database
	|	|	└── db.conf 			# environment variables for this container.
	|	├── image/				# container migrate
	|	|	├── Dockerfile 			# Contains all the comands for make image.
	|	|	└── entrypoint.sh		# entrypoint.
	| ├── test/					# container test
	|	|	├── Dockerfile			# instruction for docker.
	|	|	└── api.conf			# environment variables for this container.
	├── src/					# Source files.
	|	├── blueprints/				# Blueprints for flask (routes).
	|	├── config/				# Contains credentials for firebase.
	|	├── helpers/				# Helpers for integrate to flask.
	|	├── middlewares/  			# Middlewares as decorators.
	|	├── mixins/				# Mixins for integrate to sqlalchemy.
	|	├── models/ 				# Model for sqlalchemy.
	|	├── seed/				# Seeds
	|	├── api.py				# Entrypoint for api.
	|	├── db.py				# DB instance.
	| ├── firebase.py				# Firebase initialize app for admin and web.
	|	└── seed.py				# Manage commandline seed.
	├── requirements.txt
	├── wsgi.py					# Entrypoint for WSGI.
	├── docker-compose.yml				# Configuration that is applied to each container started for that service.
	├── Dockerfile 					# Contains all the commands for image of container api production.
	├── README.md 					# Readme of a lifetime.
	└── heroku.yml					# Config for deploy on heroku.

## Discussion 💬

* Discuss Conexperto Server on [Github Discussions](https://github.com/conexperto/server/discussions)

## Contributing 🎢

To contribute, please review the issues in the projects section [projects](https://github.com/conexperto/server/projects/1)

In order to maintain consistency and readability of commit messages, this convention is used [ConventionalCommits](https://www.conventionalcommits.org/en/v1.0.0/)

And with the help of the following hooks we can imply these conventions to the workflow.
```sh
pip install gitlint
gitlint install-hook
```

To maintain a stable & quality code, the following hooks have been used with [pre-commit](https://pre-commit.com/).

* [flake8](https://flake8.pycqa.org/en/latest/)
* [black](https://pypi.org/project/black/)
* [reorder_python_imports](https://github.com/asottile/reorder_python_imports)
* pre-commit-hooks (see file .pre-commit-config.yaml)

To install the pre-commit and use your hook configuration.
```sh
pip install pre-commit
pre-commit install
```
