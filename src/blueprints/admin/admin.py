""" src.blueprints.admin.admin """
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import has_access
from src.middlewares import login_required
from src.services import AdminService
from src.services import Privileges


router = Blueprint(name="Admin", import_name=__name__)


@router.route("/<uid>", methods=["GET"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def index_admin_one(uid):
    """
    GET: /api/v1/admin/<uid>
    """
    try:
        service = AdminService()
        user = service.get(uid)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/", methods=["GET"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def index_admin():
    """
    GET: /api/v1/admin
    """
    try:
        query = request.args.get("query")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = AdminService()
        paginate = service.list(query, page, per_pages, order_by, order)

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
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/", methods=["POST"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def register_admin():
    """
    POST: /api/v1/admin
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = AdminService()
        user = service.create(body, g.admin)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/<uid>", methods=["PUT"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def update_admin(uid):
    """
    PUT: /api/v1/admin/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = AdminService()
        user = service.update(uid, body, g.admin)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/<uid>", methods=["PATCH"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def update_field_admin(uid):
    """
    PATCH: /api/v1/admin/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = AdminService()
        user = service.update_field(uid, body, g.admin)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def disabled_admin(uid):
    """
    PATCH /api/v1/admin/disabled/<uid>
    """
    try:
        service = AdminService()
        user = service.disabled(uid, g.admin)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/<uid>", methods=["DELETE"])
@login_required(admin=True)
@has_access(Privileges.Admin)
def delete_admin(uid):
    """
    DELETE: /api/v1/admin/<uid>
    """
    try:
        service = AdminService()
        user = service.delete(uid, g.admin)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()
