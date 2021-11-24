#!/bin/bash

FLASK_APP="src.api:create_api()"

flask db upgrade
