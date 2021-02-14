from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import AuthService, \
                            ExpertService, \
                            PlanService, \
                            AssociationExpertToMethodService, \
                            AssociationExpertToSpecialityService



router = Blueprint(name='Auth', import_name=__name__)

# Decorador
def get_token():
    headers = request.headers
    prefix = 'Bearer '

    if not 'authorization' in headers:
        raise abort(401, description='NotFoundToken', response='auth/not-found-token')

    token = headers['authorization']

    if not token.startswith(prefix):
        raise abort(401, description='InvalidIdToken', response='auth/invalid-id-token')
    
    if not token[len(prefix):]:
        raise abort(401, description='InvalidIdToken', response='auth/invalid-id-token')

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
def index_auth():
    return jsonify({
        "success": True,
        "response": g.user
    })

# POST: /api/v1/auth
@router.route('/', methods=['POST'])
def register_auth():
    body = request.get_json()
    
    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = AuthService()
    user = service.create(body)

    return jsonify({'success': True, 'response': user});

# PUT: /api/v1/auth
@router.route('/', methods=['PUT'])
@login_required
def update_auth():
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = AuthService()
    user = service.update(g.user, body)

    return jsonify({'success': True, 'response': user})

# PUT: /api/v1/auth/expert
@router.route('/expert', methods=['PUT'])
@login_required
def update_auth_expert():
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    _expert = g.user['b'].expert
    
    if hasattr(body, 'speciality'):
        ass_speciality = AssociationExpertToSpecialityService()
        ass_speciality.update_or_create_many(_expert.id, body['speciality'])

    if hasattr(body, 'method'):
        ass_method = AssociationExpertToMethodService()
        ass_method.update_or_create_many(_expert.id, body['method'])

    if hasattr(body, 'plan'):
        plan = PlanService()
        plan.update_or_create_many(_expert.id, body['plan'])

    service = ExpertService()
    expert = service.update(_expert.id, body)

    return jsonify({ 'success': True, 'response': expert })

# PATCH: /api/v1/auth
@router.route('/', methods=['PATCH'])
@login_required
def update_field_auth():
    body = request.get_json()

    if not body:
        return abort(400, description='NotFoundData', response='not-found-data')

    service = AuthService()
    user = service.update_field(g.user, body)

    return jsonify({'success': True, 'response': user})

# PATCH /api/v1/auth/disabled
@router.route('/disabled', methods=['PATCH'])
@login_required
def disabled_auth():
    service = AuthService()
    user = service.disabled(g.user)

    return jsonify({ 'success': True })


# DELETE: /api/v1/auth
@router.route('/', methods=['DELETE'])
@login_required
def delete_auth():
    service = AuthService()
    service.delete(g.user)

    return jsonify({
        'success': True,
        'response': g.user
    })




