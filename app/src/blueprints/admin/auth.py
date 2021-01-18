from flask import Blueprint, g, request, jsonify
from functools import wraps
from werkzeug.exceptions import Unauthorized
from src.services.admin import AuthAdminService


router = Blueprint(name='AuthAdmin', import_name=__name__)


def get_token():
    headers = request.headers
    prefix = 'Bearer '

    if not 'authorization' in headers:
        raise Unauthorized('Not found token')

    token = headers['authorization']

    if not token.startswith(prefix):
        raise Unauthorized('Invalid token')

    return token[len(prefix):]


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError('The auth decorator needs to token_required decorator')

        service = AuthAdminService()
        g.user = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap


@router.route('/', methods=['GET'])
@login_required
def index():
    return jsonify(g.user);
