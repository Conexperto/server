from flask import Blueprint, g, request, jsonify
from functools import wraps
from werkzeug.exceptions import Unauthorized
from src.services import AuthService


router = Blueprint(name='Auth', import_name=__name__)

# Decorador
def get_token():
    headers = request.headers
    prefix = 'Bearer '

    if not 'authorization' in headers:
        raise Unauthorized('Not found token')

    token = headers['authorization']

    if not token.startswith(prefix):
        raise Unauthorized('Invalid token')

    return token[len(prefix):]

# Decorador
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError('The auth decorator needs to token_required decorator')

        service = AuthService()
        g.user = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap

# GET: /api/v1/auth
@router.route('/', methods=['GET'])
@login_required
def index():
    return jsonify(g.user);

# POST: /api/v1/auth
@router.route('/', methods=['POST'])
def register():
    body = request.json

    service = AuthService()
    service.create_user(body)

    return jsonify(service.response());

# PUT: /api/v1/auth
@router.route('/', methods=['PUT'])
def update():
    body = request.json
    user = g.user

    service = AuthService()
    service.update_user(user, body)

    return jsonify(service.response())

# PATCH: /api/v1/auth
@router.route('/', methods=['PATCH'])
def update_field():
    body = request.json
    user = g.user

    service = AuthService()
    service.update_field_user(user, body)

    return jsonify(service.response())

# DELETE: /api/v1/auth
@router.route('/', methods=['DELETE'])
def delete_user():
    user = g.user

    service = AuthService()
    service.delete_user(user)

    return jsonify(service.response())

