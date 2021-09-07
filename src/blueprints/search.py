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
        search = request.args.get("search")

        service = SearchService()
        items = service.suggestions(search)

        return jsonify({"success": True, "search": search, "response": items})
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
        search = request.args.get("search")
        speciality = request.args.get("speciality")
        page = request.args.get("page") or 1
        per_page = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = SearchService()
        paginate = service.list(search, speciality, page, per_page, order_by, order)

        return jsonify(
            {
                "success": True,
                "search": search,
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
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_page = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = SearchService()
        paginate = service.speciality(search, page, per_page, order_by, order)

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
