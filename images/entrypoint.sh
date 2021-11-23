#!/bin/bash

set -euo pipefail

FLASK_APP="src.api:create_api()" eval 'flask db upgrade'
FLASK_APP="src.api:create_api()" eval 'flask seed user up'
FLASK_APP="src.api:create_api()" eval 'flask seed admin up'

exec flask run --host=0.0.0.0
