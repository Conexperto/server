from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.services import AuthAdminService


router = Blueprint(name="AuthAdmin", import_name=__name__)


def get_token():
    headers = request.headers
    prefix = "Bearer "

    if not "authorization" in headers:
        raise abort(401, description="NotFoundToken", response="auth/not-found-token")

    token = headers["authorization"]
    if not token.startswith(prefix):
        raise abort(401, description="InvalidIdToken", response="auth/invalid-id-token")

    if not token[len(prefix) :]:
        raise abort(401, description="InvalidIdToken", response="auth/invalid-id-token")

    return token[len(prefix) :]


# Decorator
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError("The auth decorator needs to token_required decorator")

        service = AuthAdminService()
        g.admin = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap


# GET: /api/v1/admin/auth
@router.route("/", methods=["GET"])
@login_required
def index_auth_admin():
    return jsonify({"success": True, "response": g.admin})


# POST: /api/v1/admin/auth
@router.route("/", methods=["POST"])
@login_required
def register_auth_admin():
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = AuthAdminService()
    user = service.create(body)

    return jsonify({"success": True, "response": user})


# PUT: /api/v1/admin/auth
@router.route("/", methods=["PUT"])
@login_required
def update_auth_admin():
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = AuthAdminService()
    user = service.update(g.admin, body)

    return jsonify({"success": True, "response": user})


# PATCH: /api/v1/admin/auth
@router.route("/", methods=["PATCH"])
@login_required
def update_field_auth_admin():
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = AuthAdminService()
    user = service.update_field(g.admin, body)

    return jsonify({"success": True, "response": user})


# PATCH /api/v1/auth/disabled
@router.route("/disabled", methods=["PATCH"])
@login_required
def disabled_auth_admin():
    service = AuthAdminService()
    user = service.disabled(g.admin)

    return jsonify({"success": True, "response": user})


# DELETE: /api/v1/admin/auth
@router.route("/", methods=["DELETE"])
@login_required
def delete_auth_admin():
    service = AuthAdminService()
    service.delete(g.admin)

    return jsonify({"success": True, "response": g.admin})
