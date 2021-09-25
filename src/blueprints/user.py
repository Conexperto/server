""" src.blueprints.user """
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import login_required
from src.services import UserService


router = Blueprint(name="User", import_name=__name__)


@router.route("/<int:_id>", methods=["GET"])
@login_required()
def index_user_one(_id):
    """
    GET: /api/v1/user/<int:_id>
    """
    try:
        service = UserService()
        user = service.get(_id)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


@router.route("/", methods=["GET"])
@login_required()
def index_user():
    """
    GET: /api/v1/user
    """
    try:
        search = request.args.get("search")
        filter_by = request.args
        page = request.args.get("page", 1)
        per_pages = request.args.get("limit", 10)
        order_by = request.args.get("orderBy", None)
        order = parse_order(request.args.get("order", None))

        service = UserService()
        users = service.list(search, filter_by, page, per_pages, order_by, order)

        return jsonify({"success": True, "response": users})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))
