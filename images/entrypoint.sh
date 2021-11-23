#!/bin/bash
set -euo pipefail

FLASK_APP="src.api:create_api()" eval 'flask db upgrade'

exec flask run --host=0.0.0.0
