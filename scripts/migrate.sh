#!/bin/bash

FLASK_APP="src.api:create_api()"

exec flask db $1
