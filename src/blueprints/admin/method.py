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


@router.route("/<int:_id>", methods=["GET"])
@login_required(admin=True)
def index_method_admin_one(_id):
    """
    GET: /api/v1/admin/method/<int:_id>
    """
    try:
        service = MethodService()
        method = service.get(_id)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


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
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


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
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


@router.route("/<int:_id>", methods=["PUT"])
@login_required(admin=True)
def update_method_admin(_id):
    """
    PUT: /api/v1/admin/method/<int:_id>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = MethodService()
        method = service.update(_id, body)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


@router.route("/<int:_id>", methods=["PATCH"])
@login_required(admin=True)
def update_field_method_admin(_id):
    """
    PATCH: /api/v1/admin/method/<int:_id>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = MethodService()
        method = service.update_field(_id, body)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


@router.route("/disabled/<int:_id>", methods=["PATCH"])
@login_required(admin=True)
def disabled_method_admin(_id):
    """
    PATCH: /api/v1/admin/method/disabled/<int:_id>
    """
    try:
        service = MethodService()
        method = service.disabled(_id)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))


@router.route("/<int:_id>", methods=["DELETE"])
@login_required(admin=True)
def delete_method_admin(_id):
    """
    DELETE: /api/v1/admin/method/<int:_id>
    """
    try:
        service = MethodService()
        method = service.delete(_id)

        return jsonify({"success": True, "response": method})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex))
