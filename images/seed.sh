#!/bin/bash

FLASK_APP="src.api:create_api()" eval 'flask seed user up'
FLASK_APP="src.api:create_api()" eval 'flask seed admin up'
