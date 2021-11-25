#!/bin/bash

FLASK_APP="src.api:create_api()"

exec flask seed $1 $2
