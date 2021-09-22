""" src.blueprints.admin.user """
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import login_required
from src.services import UserService


router = Blueprint(name="UserAdmin", import_name=__name__)


@router.route("/<uid>", methods=["GET"])
@login_required(admin=True)
def index_user_admin_one(uid):
    """
    GET: /api/v1/admin/user/<uid>
    """
    try:
        service = UserService()
        user = service.get(uid)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_user_admin():
    """
    GET: /api/v1/admin/user
    """
    try:
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = UserService()
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
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/", methods=["POST"])
@login_required(admin=True)
def register_user_admin():
    """
    POST: /api/v1/admin/user
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = UserService()
        user = service.create(body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/<uid>", methods=["PUT"])
@login_required(admin=True)
def update_user_admin(uid):
    """
    PUT: /api/v1/admin/user/<uid>
    """
    try:
        body = request.get_json()

        if not uid:
            raise HandlerException(404, "Not found user")

        if not body:
            raise HandlerException(400, "Not found body")

        service = UserService()
        user = service.update(uid, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/<uid>", methods=["PATCH"])
@login_required(admin=True)
def update_field_user_admin(uid):
    """
    PATCH: /api/v1/admin/user/<uid>
    """
    try:
        body = request.get_json()

        if not uid:
            raise HandlerException(404, "Not found user")

        if not body:
            raise HandlerException(400, "Not found body")

        service = UserService()
        user = service.update_field(uid, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required(admin=True)
def disabled_user_admin(uid):
    """
    PATCH /api/v1/admin/user/disabled/<uid>
    """
    try:
        service = UserService()
        user = service.disabled(uid)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/<uid>", methods=["DELETE"])
@login_required(admin=True)
def delete_user_admin(uid):
    """
    DELETE: /api/v1/admin/user/<uid>
    """
    try:
        service = UserService()
        user = service.delete(uid)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)), str(ex).abort()
