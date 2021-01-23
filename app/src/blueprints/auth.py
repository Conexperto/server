from flask import Blueprint, g, request, jsonify
from functools import wraps
from werkzeug.exceptions import Unauthorized, BadRequest
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
@router.route('/auth', methods=['GET'])
@login_required
def index():
    return jsonify({
        "success": True,
        "response": g.user
    });

# POST: /api/v1/auth
@router.route('/auth', methods=['POST'])
def register():
    body = request.get_json()

    if not body:
        return BadRequest('Not found data')
   
    if not 'email' in body:
        return BadRequest('Not found email')

    if not 'password' in body:
        return BadRequest('Not found password')

    if not 'display_name' in body:
        return BadRequest('Not found display_name')

    service = AuthService()
    user = service.create_user(body)

    return jsonify({'success': True, 'response': user});

# PUT: /api/v1/auth
@router.route('/auth', methods=['PUT'])
def update():
    body = request.get_json()
    
    if not body:
        return BadRequest('Not found data')

    service = AuthService()
    user = service.update_user(g.user, body)

    return jsonify({'success': True, 'response': user})

# PATCH: /api/v1/auth
@router.route('/auth', methods=['PATCH'])
def update_field():
    body = request.get_json()

    if not body:
        return BadRequest('Not found data')

    service = AuthService()
    user = service.update_field_user(g.user, body)

    return jsonify({'success': True, 'response': user})

# DELETE: /api/v1/auth
@router.route('/auth', methods=['DELETE'])
def delete_user():

    service = AuthService()
    service.delete_user(g.user)

    return jsonify({ 
        'success': True, 
        'response': { 
            'uid': user.uid 
        }   
    })




