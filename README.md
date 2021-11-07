API Restful dyno-api
================

## Workflow

### Hooks

To maintain a stable & quality code, the following hooks have been used with [pre-commit](https://pre-commit.com/).

* [flake8](https://flake8.pycqa.org/en/latest/)
* [black](https://pypi.org/project/black/)
* [reorder_python_imports](https://github.com/asottile/reorder_python_imports)
* pre-commit-hooks (see file .pre-commit-config.yaml)

To install the pre-commit and use your hook configuration.
```sh
pip install pre-commit
pre-commit install
pre-commit --hook-type commit-msg
```

## Getting Started 💪

### Prerequisities

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)


### Instructions 🧐

Clone the repository and move to the project directory.
```sh
git clone git@gitlab.com:conexperto-workspace/server.git
```

Run build container.
```sh
docker-compose build
```

Run start container api.
```sh
docker-compose up api
```
then visit <http://localhost:5000/api/v1/>

Initialize migration of database.
```sh
docker-compose run --rm migrate flask db init
docker-compose run --rm migrate flask db migrate
docker-compose run --rm migrate flask db upgrade
```

if alterations are made in the api `src/models`, an update is necessary run this script.
```sh
docker-compose run --rm migrate flask db upgrade
```

## Seeds
```
docker-compose run --rm migrate flask seed <seed> <up|down>
```
e.g.
```
docker-compose run --rm migrate flask seed user up
```
or
```
docker-compose exec migrate flask seed admin down
```
See folder `src/seeds`.

## Testing
```
docker-compose run --rm test bash
```
For start container test.

Inside container.
```
pytest .
```
For exec all testing.

## Environment

### Environment for api.
In file `docker/api/api.conf` be all variables environment to api.
* `FLASK_RUN_PORT` 			- Set port for flask app.
* `FLASK_ENV`     			- Set env, 'production' or 'development'.
* `FLASK_DEBUG`   			- Set debug, enabled flask debug.
* `TESTING` 		  		- Set testing, enabled flask testing.
* `DATABASE_URL` 			- Set URL for connected to database.
* `FIREBASE_AUTH_EMULATOR_ADMIN_HOST` 	- Set host for emulator firebase admin.
* `FIREBASE_AUTH_EMULATOR_WEB_HOST`	- Set host for emulator firebase web.

### Environment for db
In file `docker/db/db.conf` be all variables envionment to db.
* `POSTGRES_MULTIPLE_DATABASES` 		- Set name database separate by command(,).
* `POSTGRES_PORT` 				- Set port, default `5432`.
* `POSTGRES_USER`				- Set user, default `owner`.
* `POSTGRES_PASSWORD`   			- Set password, defaullt `token.01`.

### Environment for migrate.
In file `docker/migrate/migrate.conf` be all variables environment to migrate.
* `FLASK_RUN_PORT` 			- Set port for flask app.
* `FLASK_ENV`     			- Set env, 'production' or 'development'.
* `FLASK_DEBUG`   			- Set debug, enabled flask debug.
* `TESTING` 				- Set testing, enabled flask testing.
* `DATABASE_URL` 			- Set URL for connected to database.
* `FIREBASE_AUTH_EMULATOR_ADMIN_HOST` 	- Set host for emulator firebase admin.
* `FIREBASE_AUTH_EMULATOR_WEB_HOST`	- Set host for emulator firebase web.

### Environment for migrate.
In file `docker/test/test.conf` be all variables environment to test.
* `FLASK_RUN_PORT` 			- Set port for flask app.
* `FLASK_ENV`     			- Set env, 'production' or 'development'.
* `FLASK_DEBUG`   			- Set debug, enabled flask debug.
* `TESTING` 				- Set testing, enabled flask testing.
* `DATABASE_URL` 			- Set URL for connected to database.
* `FIREBASE_AUTH_EMULATOR_ADMIN_HOST` 	- Set host for emulator firebase admin.
* `FIREBASE_AUTH_EMULATOR_WEB_HOST`	- Set host for emulator firebase web.
* `FIREBASE_API_KEY_ADMIN` 		- Set api key for authentication testing admin.
* `FIREBASE_API_KEY_WEB` 		- Set api key for authentication testing web.

## Folder Structure

	.
	├── docker/ 					# resource for docker-compose
	|	├── api/				# container api
	|	|	├── Dockerfile 			# Contains all the comands for make image of container api.
	|	|	└── api.conf 			# environment variables for this container.
	| ├── db/					# container db
	|	|	├── pg-init-scripts/
	|	|	|	└── create-multiple-postgresql-database.sh # script for handle multiple database
	|	|	└── db.conf 			# environment variables for this container.
	|	├── migrate/				# container migrate
	|	|	├── Dockerfile 			# instruction for docker.
	|	|	└── migrate.conf		# environment variables for this container.
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
