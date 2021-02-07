from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import AuthService, UserService
from src.models import Privilegies


router = Blueprint(name='User', import_name=__name__)

# Decorador
def get_token():
    headers = request.headers
    prefix = 'Bearer '

    if not 'authorization' in headers:
        raise abort(400, description='NotFoundToken', response='auth/not-found-token')

    token = headers['authorization']

    if not token.startswith(prefix):
        raise abort(400, description='InvalidIdToken', response='auth/invalid-id-token')
    
    if not token[len(prefix):]:
        raise abort(400, description='InvalidIdToken', response='auth/invalid-id-token')

    return token[len(prefix):]

# Decorador
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError('The auth decorator needs to token_required decorator')

        service = AuthService()
        g.admin = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap

# Decorator
def has_access(func, access_level):
    @wraps
    def wrap(*arg, **kwargs):
        user = g.admin['b']
        
        if not user.has_access(access_level.value):
            abort(401, description='Unauthorized', response='You not enough permissions to access')

    return wrap

# GET: /api/v1/user/<uid>
@router.route('/<uid>', methods=['GET'])
@login_required
def index_user_one(uid):
    service = UserService()
    user = service.get_user(uid)

    return jsonify({
        "success": True,
        "response": user
    })

# GET: /api/v1/user
@router.route('/', methods=['GET'])
@login_required
def index_user():
    page = request.args.get('page') or 1
    
    service = UserService()
    users = service.list_user(page)
    
    return jsonify({
        "success": True,
        "response": users
    })

# POST: /api/v1/user
@router.route('/', methods=['POST'])
@login_required
def register_user():
    body = request.get_json()
    
    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = UserService()
    user = service.create_user(body)

    return jsonify({ 'success': True, 'response': user });

# PUT: /api/v1/user/<uid>
@router.route('/<uid>', methods=['PUT'])
@login_required
def update_user(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = UserService()
    user = service.update_user(uid, body)

    return jsonify({ 'success': True, 'response': user })

# PATCH: /api/v1/user/<uid>
@router.route('/<uid>', methods=['PATCH'])
@login_required
def update_field_user(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = UserService()
    user = service.update_field_user(uid, body)

    return jsonify({ 'success': True, 'response': user })

# PATCH /api/v1/user/disabled/<uid>
@router.route('/disabled/<uid>', methods=['PATCH'])
@login_required
def disabled_user(uid):
    service = UserService()
    user = service.disabled_user(uid)

    return jsonify({ 'success': True, 'response': user })

# DELETE: /api/v1/user/<uid>
@router.route('/<uid>', methods=['DELETE'])
@login_required
def delete_user(uid):
    service = UserService()
    user = service.delete_user(uid)

    return jsonify({
        'success': True,
        'response': user
    })
