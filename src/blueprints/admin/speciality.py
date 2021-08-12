"""
    Blueprint Speciality
"""
from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.services import AuthAdminService
from src.services import SpecialityService


router = Blueprint(name="SpecialityAdmin", import_name=__name__)


def get_token():
    """
    Decorator get_token
    """
    headers = request.headers
    prefix = "Bearer "

    if "authorization" not in headers:
        raise abort(400, description="NotFoundToken", response="auth/not-found-token")

    token = headers["authorization"]

    if not token.startswith(prefix):
        raise abort(400, description="InvalidIdToken", response="auth/invalid-id-token")

    if not token[len(prefix) :]:
        raise abort(400, description="InvalidIdToken", response="auth/invalid-id-token")

    return token[len(prefix) :]


def login_required(func):
    """
    Decorator login_required
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError("The auth decorator needs to token_required decorator")

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
def index_speciality_admin_one(uid):
    """
    GET: /api/v1/admin/speciality/<uid>
    """
    service = SpecialityService()
    speciality = service.get(uid)

    return jsonify({"success": True, "response": speciality})


@router.route("/", methods=["GET"])
@login_required
def index_speciality_admin():
    """
    GET: /api/v1/admin/speciality
    """
    page = request.args.get("page") or 1
    per_pages = request.args.get("per_pages")

    service = SpecialityService()
    specialities = service.list(page, per_pages)

    return jsonify({"success": True, "response": specialities})


@router.route("/", methods=["POST"])
@login_required
def register_speciality_admin():
    """
    POST: /api/v1/admin/speciality
    """
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = SpecialityService()
    speciality = service.create(body)

    return jsonify({"success": True, "response": speciality})


@router.route("/<uid>", methods=["PUT"])
@login_required
def update_speciality_admin(uid):
    """
    PUT: /api/v1/admin/speciality/<uid>
    """
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = SpecialityService()
    speciality = service.update(uid, body)

    return jsonify({"success": True, "response": speciality})


@router.route("/<uid>", methods=["PATCH"])
@login_required
def update_field_speciality_admin(uid):
    """
    PATCH: /api/v1/admin/speciality/<uid>
    """
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = SpecialityService()
    speciality = service.update_field(uid, body)

    return jsonify({"success": True, "response": speciality})


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required
def disabled_speciality_admin(uid):
    """
    PATCH: /api/v1/admin/speciality/disabled/<uid>
    """
    service = SpecialityService()
    speciality = service.disabled(uid)

    return jsonify({"success": True, "response": speciality})


@router.route("/<uid>", methods=["DELETE"])
@login_required
def delete_speciality_admin(uid):
    """
    DELETE: /api/v1/admin/speciality/<uid>
    """
    service = SpecialityService()
    speciality = service.delete(uid)

    return jsonify({"success": True, "response": speciality})
