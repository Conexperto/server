from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import AuthAdminService, MethodService
from src.models import Privilegies


router = Blueprint(name='MethodAdmin', import_name=__name__)

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

# GET: /api/v1/admin/method/<uid>
@router.route('/<uid>', methods=['GET'])
@login_required
def index_method_admin_one(uid):
    service = MethodService()
    method = service.get(uid)

    return jsonify({
        "success": True,
        "response": method
    })

# GET: /api/v1/admin/method
@router.route('/', methods=['GET'])
@login_required
def index_method_admin():
    search = request.args.get('search')
    page = request.args.get('page') or 1
    per_page = request.args.get('limit')
    order_by = request.args.get('orderBy')
    order = request.args.get('order')
    
    service = MethodService()
    paginate = service.list(search, page, per_page, order_by, order)
    
    return jsonify({
        "success": True,
        "response": paginate.items,
        "total": paginate.total,
        "page": paginate.page,
        "limit": paginate.per_page,
        "next": paginate.next_num
    })

# POST: /api/v1/admin/method
@router.route('/', methods=['POST'])
@login_required
def register_method_admin():
    body = request.get_json()
    
    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = MethodService()
    method = service.create(body)

    return jsonify({ 'success': True, 'response': method });

# PUT: /api/v1/admin/method/<uid>
@router.route('/<uid>', methods=['PUT'])
@login_required
def update_method_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = MethodService()
    method = service.update(uid, body)

    return jsonify({ 'success': True, 'response': method })

# PATCH: /api/v1/admin/method/<uid>
@router.route('/<uid>', methods=['PATCH'])
@login_required
def update_field_method_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = MethodService()
    method = service.update_field(uid, body)

    return jsonify({ 'success': True, 'response': method })

# PATCH /api/v1/admin/method/disabled/<uid>
@router.route('/disabled/<uid>', methods=['PATCH'])
@login_required
def disabled_method_admin(uid):
    service = MethodService()
    method = service.disabled(uid)

    return jsonify({ 'success': True, 'response': method })

# DELETE: /api/v1/admin/method/<uid>
@router.route('/<uid>', methods=['DELETE'])
@login_required
def delete_method_admin(uid):
    service = MethodService()
    method = service.delete(uid)

    return jsonify({
        'success': True,
        'response': method
    })
