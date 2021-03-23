from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import AuthService, ExpertService


router = Blueprint(name='Expert', import_name=__name__)

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

# GET: /api/v1/expert/<uid>
@router.route('/<uid>', methods=['GET'])
def index_expert_one(uid):
    service = ExpertService()
    expert = service.get(uid)

    return jsonify({
        "success": True,
        "response": expert
    })

# GET: /api/v1/expert
@router.route('/', methods=['GET'])
def index_expert():
    search = request.args.get('search')
    page = request.args.get('page') or 1
    per_page = request.args.get('limit') or 10
    order_by = request.args.get('orderBy')
    order = request.args.get('order')
    
    service = ExpertService()
    paginate = service.list(search, page, per_page, order_by, order)
    
    return jsonify({
        "success": True,
        "response": paginate.items,
        "total": paginate.total,
        "page": paginate.page,
        "limit": paginate.per_page,
        "next": paginate.next_num
    })



