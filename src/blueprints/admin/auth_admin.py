""" src.blueprints.admin.auth_admin """
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.middlewares import login_required
from src.services import AuthAdminService


router = Blueprint(name="AuthAdmin", import_name=__name__)


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_auth_admin():
    """
    GET: /api/v1/admin/auth
    """
    return jsonify({"success": True, "response": g.admin})


@router.route("/", methods=["PUT"])
@login_required(admin=True)
def update_auth_admin():
    """
    PUT: /api/v1/admin/auth
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = AuthAdminService()
        user = service.update(g.admin, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/", methods=["PATCH"])
@login_required(admin=True)
def update_field_auth_admin():
    """
    PATCH: /api/v1/admin/auth
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = AuthAdminService()
        user = service.update_field(g.admin, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()


@router.route("/disabled", methods=["PATCH"])
@login_required(admin=True)
def disabled_auth_admin():
    """
    PATCH /api/v1/auth/disabled
    """
    try:
        service = AuthAdminService()
        user = service.disabled(g.admin)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex)).abort()
