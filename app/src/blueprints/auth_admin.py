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

# Decorator
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError('The auth decorator needs to token_required decorator')

        service = AuthAdminService()
        g.admin = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap

# GET: /api/v1/admin/auth
@router.route('/auth', methods=['GET'])
@login_required
def index():
    return jsonify({
            "success": True,
            "response": g.admin
        })

# POST: /api/v1/admin/auth
@router.route('/auth', methods=['POST'])
def register():
    body = request.get_json()
    
    if not body:
        return BadRequest('Not found data')

    service = AuthService()
    user = service.create_user(body)

    return jsonify({'success': True, 'response': user});

# PUT: /api/v1/admin/auth
@router.route('/auth', methods=['PUT'])
@login_required
def update():
    body = request.get_json()

    if not body:
        return BadRequest('Not found data')

    service = AuthService()
    user = service.update_user(g.admin, body)

    return jsonify({'success': True, 'response': user})

# PATCH: /api/v1/admin/auth
@router.route('/auth', methods=['PATCH'])
@login_required
def update_field():
    body = request.get_json()

    if not body:
        return BadRequest('Not found data')

    service = AuthService()
    user = service.update_field_user(g.admin, body)

    return jsonify({'success': True, 'response': user})

# DELETE: /api/v1/admin/auth
@router.route('/auth', methods=['DELETE'])
@login_required
def delete_user():
    service = AuthService()
    service.delete_user(g.admin)

    return jsonify({
        'success': True,
        'response': {
            'uid': g.user.uid
        }
    })
