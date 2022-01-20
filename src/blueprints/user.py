""" src.blueprints.user """
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.services import UserService


router = Blueprint(name="Users", import_name=__name__)


@router.route("/<uid>", methods=["GET"])
def index_user_one(uid):
    """
    GET: /api/v1/users/<uid>
    """
    try:
        service = UserService()
        user = service.get(uid)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/", methods=["GET"])
def index_user():
    """
    GET: /api/v1/users
    """
    try:
        search = request.args.get("search", None)
        filter_by = request.args
        page = request.args.get("page", 1)
        per_pages = request.args.get("limit", 10)
        order_by = request.args.get("orderBy", None)
        order = parse_order(request.args.get("order", None))

        _filter_by = {"disabled": False, **filter_by}

        service = UserService()
        paginate = service.list(
            search, _filter_by, page, per_pages, order_by, order
        )

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
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()
