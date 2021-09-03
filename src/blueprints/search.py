from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.services import SearchService


router = Blueprint(name="Search", import_name=__name__)


@router.route("/suggestions", methods=["GET"])
def index_suggestion():
    """
    GET: /api/v1/search/suggestions
    """
    try:
        query = request.args.get("query")

        service = SearchService()
        items = service.suggestions(query)

        return jsonify({"success": True, "query": query, "response": items})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["GET"])
def index_search():
    """
    GET: /api/v1/search
    """
    try:
        query = request.args.get("query")
        speciality = request.args.get("speciality")
        page = request.args.get("page") or 1
        per_page = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = SearchService()
        paginate = service.list(query, speciality, page, per_page, order_by, order)

        return jsonify(
            {
                "success": True,
                "query": query,
                "response": paginate.items,
                "total": paginate.total,
                "page": paginate.page,
                "limit": paginate.per_page,
                "next": paginate.next_num,
            }
        )
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/speciality", methods=["GET"])
def index_search_speciality():
    """
    GET: /api/v1/search/speciality
    """
    try:
        query = request.args.get("query")
        page = request.args.get("page") or 1
        per_page = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = SearchService()
        paginate = service.speciality(query, page, per_page, order_by, order)

        return jsonify(
            {
                "success": True,
                "response": paginate.items,
                "total": paginate.total,
                "page": paginate.page,
                "limit": paginate.per_page,
                "next": paginate.next_num,
            }
        )
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))
