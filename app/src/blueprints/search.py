from flask import Blueprint, g, request, jsonify, abort
from src.services import SearchService 


router = Blueprint(name='Search', import_name=__name__)

# GET: /api/v1/search/suggestions
@router.route('/suggestions', methods=['GET'])
def index_suggestion():
    query = request.args.get('query')

    service = SearchService()
    items = service.suggestions(query)
    
    return jsonify({
        "success": True,
        "query": query,
        "response": items,
    })

# GET: /api/v1/search
@router.route('/', methods=['GET'])
def index_search():
    query = request.args.get('query')
    speciality = request.args.get('speciality')
    page = request.args.get('page') or 1
    per_page = request.args.get('limit') or 10
    order_by = request.args.get('orderBy') or 'created_at'
    order = request.args.get('order') or 'desc'
    
    service = SearchService()
    paginate = service.list(query,
                                speciality,
                                page, 
                                per_page, 
                                order_by, 
                                order)
    
    return jsonify({
        "success": True,
        "query": query,
        "speciality": speciality,
        "response": paginate.items,
        "total": paginate.total,
        "page": paginate.page,
        "limit": paginate.per_page,
        "next": paginate.next_num
    })



