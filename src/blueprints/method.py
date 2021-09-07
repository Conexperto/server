from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.services import MethodService


router = Blueprint(name="Method", import_name=__name__)


@router.route("/<int:_id>", methods=["GET"])
def index_method_one(_id):
    """
    GET: /api/v1/method/<int:_id>
    """
    try:
        service = MethodService()
        speciality = service.get(_id)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["GET"])
def index_method():
    """
    GET: /api/v1/method
    """
    try:
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_page = request.args.get("limit") or 10
        order_by = request.args.get("orderBy")
        order = parse_order(request.args.get("order"))

        service = MethodService()
        paginate = service.list(search, page, per_page, order_by, order)

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
