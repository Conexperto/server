from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import AuthAdminService, UserService
from src.models import Privilegies


router = Blueprint(name='UserAdmin', import_name=__name__)

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

        service = AuthAdminService()
        g.admin = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap

# Decorator
def has_access(func, access_level):
    @wraps(func)
    def wrap(*arg, **kwargs):
        user = g.admin['b']
        
        if not user.has_access(access_level.value):
            abort(401, description='Unauthorized', response='You not enough permissions to access')

    return wrap

# GET: /api/v1/admin/user/<uid>
@router.route('/<uid>', methods=['GET'])
@login_required
def index_user_admin_one(uid):
    service = UserService()
    user = service.get(uid)

    return jsonify({
        "success": True,
        "response": user
    })

# GET: /api/v1/admin/user
@router.route('/', methods=['GET'])
@login_required
def index_user_admin():
    page = request.args.get('page') or 1
    per_pages = request.args.get('per_pages')
    
    service = UserService()
    users = service.list(page, per_pages)
    
    return jsonify({
        "success": True,
        "response": users
    })

# POST: /api/v1/admin/user
@router.route('/', methods=['POST'])
@login_required
def register_user_admin():
    body = request.get_json()
    
    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = UserService()
    user = service.create(body)

    return jsonify({ 'success': True, 'response': user })

# PUT: /api/v1/admin/user/<uid>
@router.route('/<uid>', methods=['PUT'])
@login_required
def update_user_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = UserService()
    user = service.update(uid, body)

    return jsonify({ 'success': True, 'response': user })

# PATCH: /api/v1/admin/user/<uid>
@router.route('/<uid>', methods=['PATCH'])
@login_required
def update_field_user_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = UserService()
    user = service.update_field(uid, body)

    return jsonify({ 'success': True, 'response': user })

# PATCH /api/v1/admin/user/disabled/<uid>
@router.route('/disabled/<uid>', methods=['PATCH'])
@login_required
def disabled_user_admin(uid):
    service = UserService()
    user = service.disabled(uid)

    return jsonify({ 'success': True, 'response': user })

# DELETE: /api/v1/admin/user/<uid>
@router.route('/<uid>', methods=['DELETE'])
@login_required
def delete_user_admin(uid):
    service = UserService()
    user = service.delete(uid)

    return jsonify({
        'success': True,
        'response': user
    })
