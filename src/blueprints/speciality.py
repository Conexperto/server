from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.services import SpecialityService


router = Blueprint(name="Speciality", import_name=__name__)


@router.route("/<int:_id>", methods=["GET"])
def index_speciality_one(_id):
    """
    GET: /api/v1/speciality/<int:_id>
    """
    try:
        service = SpecialityService()
        speciality = service.get(_id)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


# GET: /api/v1/speciality
@router.route("/", methods=["GET"])
def index_speciality():
    """
    GET: /api/v1/speciality
    """
    try:
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        if str(order).isnumeric():
            order = int(order)
            if order == 1:
                order = "asc"
            if order == -1:
                order = "desc"

        service = SpecialityService()
        paginate = service.list(search, page, per_pages, order_by, order)

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
