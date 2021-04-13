from flask import Blueprint, g, request, jsonify, abort
from src.services import SearchService 


router = Blueprint(name='Search', import_name=__name__)

# GET: /api/v1/search/suggestions
@router.route('/suggestions', methods=['GET'])
def index_suggestion():
    search = request.args.get('search')
    service = SearchService()
    search = service.suggestions(search)

    return jsonify({
        "success": True,
        "response": search
    })

# GET: /api/v1/search
@router.route('/', methods=['GET'])
def index_search():
    search = request.args.get('search')
    page = request.args.get('page') or 1
    per_page = request.args.get('limit') or 10
    order_by = request.args.get('orderBy')
    order = request.args.get('order')
    
    service = SearchService()
    paginate = service.list(search, page, per_page, order_by, order)
    
    return jsonify({
        "success": True,
        "response": paginate.items,
        "total": paginate.total,
        "page": paginate.page,
        "limit": paginate.per_page,
        "next": paginate.next_num
    })



