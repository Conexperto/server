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
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_user_admin():
    """
    GET: /api/v1/admin/user
    """
    try:
        query = request.args.get("query")
        page = request.args.get("page") or 1
        per_pages = request.args.get("per_pages")
        order_by = request.args.get("orderBy")
        order = parse_order(request.args.get("order"))

        service = UserService()
        users = service.list(query, page, per_pages, order_by, order)

        return jsonify({"success": True, "response": users})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["POST"])
@login_required(admin=True)
def register_user_admin():
    """
    POST: /api/v1/admin/user
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = UserService()
        user = service.create(body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PUT"])
@login_required(admin=True)
def update_user_admin(uid):
    """
    PUT: /api/v1/admin/user/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = UserService()
        user = service.update(uid, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PATCH"])
@login_required(admin=True)
def update_field_user_admin(uid):
    """
    PATCH: /api/v1/admin/user/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = UserService()
        user = service.update_field(uid, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


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
        HandlerException(500, "Unexpected response: " + str(ex))


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
        HandlerException(500, "Unexpected response: " + str(ex))
