from flask import Blueprint, g, request, jsonify, abort
from functools import wraps
from src.services import MethodService 


router = Blueprint(name='Method', import_name=__name__)

# GET: /api/v1/method/<int:id>
@router.route('/<int:id>', methods=['GET'])
def index_speciality_one(_id):
    service = SpecialityService()
    speciality = service.get(_id)

    return jsonify({
        "success": True,
        "response": speciality
    })

# GET: /api/v1/method
@router.route('/', methods=['GET'])
def index_speciality():
    search = request.args.get('search')
    page = request.args.get('page') or 1
    per_page = request.args.get('limit') or 10
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

