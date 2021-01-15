API Restful dyno-api
================

## Getting Started

### Prerequisities

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)


### Instructions

Clone the repository and move to the project directory.
```sh
git clone 
cd api
```

Run build container.
```sh
docker-compose build
```

Run start container.
```sh
docker-compose up
```

Or run this command for start and build container.
```sh
docker-compose up --build
```
then visit <http://localhost:3000/api/v1/>

Initialize migration of database.
```sh
docker-compose run --rm api python3 manage.py db init
docker-compose run --rm api python3 manage.py db migrate
docker-compose run --rm api python3 manage.py db upgrade
```

if alterations are made in the api `app/src/models`, an update is necessary run this script.
```sh
docker-compose run --rm api python3 manage.py upgrade
```

Alternative for run all command, directly inside container api.
```sh
docker-compose run --rm api bash
```

## Environment

### Environment for api.
In file api.conf be all variables environment to api.
* `ENV`     		- Set env, 'production' or 'development'.
* `DEBUG`   		- Set debug, enabled flask debug. 
* `TESTING` 		- Set testing, enabled flask testing. 

Sqlalchemy connect to db container.
* `POSTGRES_HOST` 	  - Set host, default `db`.
* `POSTGRES_PORT`     - Set port, default `5432`.
* `POSTGRES_DB`		  - Set dbname, default `conexpert`.
* `POSTGRES_USER`     - Set user, default `owner`.
* `POSTGRES_PASSWORD` - Set password, default `token.01`.

### Environment for db
In file database.conf be all variables envionment to db.
* `POSTGRES_PORT` 		- Set port, default `5432`.
* `POSTGRES_DB`			- Set dbname, default `conexpert`.
* `POSTGRES_USER`		- Set user, default `owner`.
* `POSTGRES_PASSWORD`   - Set password, defaullt `token.01`.

## Folder Structure

	.
	├── app 
	|	├── hooks					# Contains all resource external.
	|	├── src						# Source files.
	|	|	├── blueprints			# Blueprints for flask (routes).
	|	|	├── helpers				# Helpers for integrate to flask.
	|	|	├── mixins				# Mixins for integrate to sqlalchemy. 
	|	|	├── models 				# Model for sqlalchemy.
	|	|	├── api.py				# Entrypoint for api. 
	|	|	└── db.py				# DB instance.
	|	├── static					# Contains all resource static
	|	├── templates				# Templates 
	|	├── test					# Unit tests.
	|	├── config.py				# Catch all environment variables to flask.
	|	├── manage.py				# Manage migrate of database. 
	|	├── requirements.txt		# pip requirements.txt 
	|	├── run.py 					# Entrypoint for run app with python3  
	|	├── test.py					# Entrypoint for exec unitesting
	|	└── wsgi.py					# Entrypoint for WSGI
	├── api.conf					# Environment container api.
	├── db.conf		 				# Environment container db.
	├── docker-compose.yml			# Configuration that is applied to each container started for that service.
	├── Dockerfile 					# Contains all the commands for image of container api.
	├── README.md 					# Readme of a lifetime.
	└── heroku.yml					# 

## Deploy

### Prerequisities

In order to deploy this container you'll need heroku installed. [Here the information on how to install it and login](https://devcenter.heroku.com/articles/heroku-cli) 


### Instructions

Set the stack of your app to container.
```
heroku stack:set container
```

Push your app to Heroku.
```
git push heroku master
```
=======
# Dino API

>>>>>>> a23e8fa1ec50411755daf757ed6c28f7d4600360
