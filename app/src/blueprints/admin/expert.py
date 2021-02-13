from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import AuthAdminService, \
                            ExpertService, \
                            PlanService, \
                            AssociationExpertToSpecialityService, \
                            AssociationExpertToMethodService
from src.models import Privilegies


router = Blueprint(name='ExpertAdmin', import_name=__name__)

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

# GET: /api/v1/admin/expert/<uid>
@router.route('/<uid>', methods=['GET'])
@login_required
def index_expert_admin_one(uid):
    service = ExpertService()
    expert = service.get(uid)

    return jsonify({
        "success": True,
        "response": expert
    })

# GET: /api/v1/admin/expert
@router.route('/', methods=['GET'])
@login_required
def index_expert_admin():
    page = request.args.get('page') or 1
    per_pages = request.args.get('per_pages')

    service = ExpertService()
    experts = service.list(page, per_pages)
    
    return jsonify({
        "success": True,
        "response": experts
    })

# POST: /api/v1/admin/expert
@router.route('/', methods=['POST'])
@login_required
def register_expert_admin():
    body = request.get_json()
    
    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = ExpertService()
    expert = service.create(body)

    return jsonify({ 
        "success": True, 
        "response": expert 
    });

# PUT: /api/v1/admin/expert/<uid>
@router.route('/<uid>', methods=['PUT'])
@login_required
def update_expert_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = ExpertService()
    expert = service.update(uid, body)

    if hasattr(body, 'speciality'):
        ass_speciality = AssociationExpertToSpecialityService()
        ass_speciality.update_or_create_and_delete_many(expert.id, body['speciality'])
    if hasattr(body, 'method'):
        ass_method = AssociationExpertToMethodService()
        ass_method.update_or_create_and_delete_many(expert.id, body['method'])
    if hasattr(body, 'plan'):
        plan = PlanService()
        plan.update_or_create_and_delete_many(expert.id, body['plan'])

    return jsonify({ 'success': True, 'response': service.get(expert.id) })

# PATCH: /api/v1/admin/expert/<uid>
@router.route('/<uid>', methods=['PATCH'])
@login_required
def update_field_expert_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = ExpertService()
    expert = service.update_field(uid, body)

    if hasattr(body, 'speciality'):
        ass_speciality = AssociationExpertToSpecialityService()
        ass_speciality.update_or_create_and_delete_many(expert.id, body['speciality'])
    if hasattr(body, 'method'):
        ass_method = AssociationExpertToMethodService()
        ass_method.update_or_create_and_delete_many(expert.id, body['method'])
    if hasattr(body, 'plan'):
        plan = PlanService()
        plan.update_or_create_and_delete_many(expert.id, body['plan'])

    return jsonify({ 'success': True, 'response': service.get(expert.id) })

# PATCH /api/v1/admin/expert/disabled/<uid>
@router.route('/disabled/<uid>', methods=['PATCH'])
@login_required
def disabled_expert_admin(uid):
    service = ExpertService()
    expert = service.disabled(uid)

    return jsonify({ 'success': True, 'response': expert })

# DELETE: /api/v1/admin/expert/<uid>
@router.route('/<uid>', methods=['DELETE'])
@login_required
def delete_expert_admin(uid):
    service = ExpertService()
    expert = service.delete(uid)

    return jsonify({
        'success': True,
        'response': expert
    })
