"""
    Blueprint Method
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import login_required
from src.services import MethodService


router = Blueprint(name="MethodAdmin", import_name=__name__)


@router.route("/<uid>", methods=["GET"])
@login_required(admin=True)
def index_method_admin_one(uid):
    """
    GET: /api/v1/admin/method/<uid>
    """
    try:
        service = MethodService()
        method = service.get(uid)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_method_admin():
    """
    GET: /api/v1/admin/method
    """
    try:
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = MethodService()
        methods = service.list(search, page, per_pages, order_by, order)

        return jsonify({"success": True, "response": methods})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["POST"])
@login_required(admin=True)
def register_method_admin():
    """
    POST: /api/v1/admin/method
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = MethodService()
        method = service.create(body)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PUT"])
@login_required(admin=True)
def update_method_admin(uid):
    """
    PUT: /api/v1/admin/method/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = MethodService()
        method = service.update(uid, body)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PATCH"])
@login_required(admin=True)
def update_field_method_admin(uid):
    """
    PATCH: /api/v1/admin/method/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = MethodService()
        method = service.update_field(uid, body)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required(admin=True)
def disabled_method_admin(uid):
    """
    PATCH: /api/v1/admin/method/disabled/<uid>
    """
    try:
        service = MethodService()
        method = service.disabled(uid)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["DELETE"])
@login_required(admin=True)
def delete_method_admin(uid):
    """
    DELETE: /api/v1/admin/method/<uid>
    """
    try:
        service = MethodService()
        method = service.delete(uid)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))
