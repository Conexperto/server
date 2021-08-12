""" src.blueprints.admin.user """
from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request
from src.services import AuthAdminService
from src.services import UserService


router = Blueprint(name="UserAdmin", import_name=__name__)


def get_token():
    """
    Decorator get_token
    """
    headers = request.headers
    prefix = "Bearer "

    if "authorization" not in headers:
        raise abort(
            400, description="NotFoundToken", response="auth/not-found-token"
        )

    token = headers["authorization"]

    if not token.startswith(prefix):
        raise abort(
            400, description="InvalidIdToken", response="auth/invalid-id-token"
        )

    if not token[len(prefix) :]:
        raise abort(
            400, description="InvalidIdToken", response="auth/invalid-id-token"
        )

    return token[len(prefix) :]


def login_required(func):
    """
    Decorator login_required
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError(
                "The auth decorator needs to token_required decorator"
            )

        service = AuthAdminService()
        g.admin = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap


def has_access(func, access_level):
    """
    Decorator has_access
    """

    @wraps(func)
    def wrap():
        user = g.admin["b"]

        if not user.has_access(access_level.value):
            abort(
                401,
                description="Unauthorized",
                response="You not enough permissions to access",
            )

    return wrap


@router.route("/<uid>", methods=["GET"])
@login_required
def index_user_admin_one(uid):
    """
    GET: /api/v1/admin/user/<uid>
    """
    service = UserService()
    user = service.get(uid)

    return jsonify({"success": True, "response": user})


@router.route("/", methods=["GET"])
@login_required
def index_user_admin():
    """
    GET: /api/v1/admin/user
    """
    page = request.args.get("page") or 1
    per_pages = request.args.get("per_pages")

    service = UserService()
    users = service.list(page, per_pages)

    return jsonify({"success": True, "response": users})


@router.route("/", methods=["POST"])
@login_required
def register_user_admin():
    """
    POST: /api/v1/admin/user
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    service = UserService()
    user = service.create(body)

    return jsonify({"success": True, "response": user})


@router.route("/<uid>", methods=["PUT"])
@login_required
def update_user_admin(uid):
    """
    PUT: /api/v1/admin/user/<uid>
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    service = UserService()
    user = service.update(uid, body)

    return jsonify({"success": True, "response": user})


@router.route("/<uid>", methods=["PATCH"])
@login_required
def update_field_user_admin(uid):
    """
    PATCH: /api/v1/admin/user/<uid>
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    service = UserService()
    user = service.update_field(uid, body)

    return jsonify({"success": True, "response": user})


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required
def disabled_user_admin(uid):
    """
    PATCH /api/v1/admin/user/disabled/<uid>
    """
    service = UserService()
    user = service.disabled(uid)

    return jsonify({"success": True, "response": user})


@router.route("/<uid>", methods=["DELETE"])
@login_required
def delete_user_admin(uid):
    """
    DELETE: /api/v1/admin/user/<uid>
    """
    service = UserService()
    user = service.delete(uid)

    return jsonify({"success": True, "response": user})
