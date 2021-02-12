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

# GET: /api/v1/expert/<int:id>
@router.route('/<int:id>', methods=['GET'])
@login_required
def index_expert_one(_id):
    service = ExpertService()
    expert = service.get(_id)

    return jsonify({
        "success": True,
        "response": expert
    })

# GET: /api/v1/expert
@router.route('/', methods=['GET'])
@login_required
def index_expert():
    page = request.args.get('page') or 1
    per_pages = request.args.get('per_pages')

    service = ExpertService()
    expets = service.list(page, per_pages)
    
    return jsonify({
        "success": True,
        "response": experts
    })





