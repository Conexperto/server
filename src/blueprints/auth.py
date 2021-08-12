"""
    Blueprint Auth
"""
from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request
from src.services import AssociationExpertToMethodService
from src.services import AssociationExpertToSpecialityService
from src.services import AuthService
from src.services import ExpertService
from src.services import PlanService


router = Blueprint(name="Auth", import_name=__name__)


def get_token():
    """
    Decorador get_token
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
    Decorador login_required
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        id_token = get_token()

        if not id_token:
            raise TypeError(
                "The auth decorator needs to token_required decorator"
            )

        service = AuthService()
        g.user = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap


@router.route("/", methods=["GET"])
@login_required
def index_auth():
    """
    GET: /api/v1/auth
    """
    return jsonify({"success": True, "response": g.user})


@router.route("/", methods=["POST"])
def register_auth():
    """
    POST: /api/v1/auth
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    service = AuthService()
    user = service.create(body)

    return jsonify({"success": True, "response": user})


@router.route("/", methods=["PUT"])
@login_required
def update_auth():
    """
    PUT: /api/v1/auth
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    service = AuthService()
    user = service.update(g.user, body)

    return jsonify({"success": True, "response": user})


@router.route("/expert", methods=["PUT"])
@login_required
def update_auth_expert():
    """
    PUT: /api/v1/auth/expert
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    _expert = g.user["b"].expert

    if hasattr(body, "speciality"):
        ass_speciality = AssociationExpertToSpecialityService()
        ass_speciality.update_or_create_and_delete_many(
            _expert.id, body["speciality"]
        )

    if hasattr(body, "method"):
        ass_method = AssociationExpertToMethodService()
        ass_method.update_or_create_and_delete_many(_expert.id, body["method"])

    if hasattr(body, "plan"):
        plan = PlanService()
        plan.update_or_create_and_delete_many(_expert.id, body["plan"])

    service = ExpertService()
    expert = service.update(_expert.id, body)

    return jsonify({"success": True, "response": expert})


@router.route("/", methods=["PATCH"])
@login_required
def update_field_auth():
    """
    PATCH: /api/v1/auth
    """
    body = request.get_json()

    if not body:
        return abort(
            400, description="NotFoundData", response="not-found-data"
        )

    service = AuthService()
    user = service.update_field(g.user, body)

    return jsonify({"success": True, "response": user})


@router.route("/disabled", methods=["PATCH"])
@login_required
def disabled_auth():
    """
    PATCH /api/v1/auth/disabled
    """
    service = AuthService()
    user = service.disabled(g.user)

    return jsonify({"success": True, "response": user})


@router.route("/", methods=["DELETE"])
@login_required
def delete_auth():
    """
    DELETE: /api/v1/auth
    """
    service = AuthService()
    service.delete(g.user)

    return jsonify({"success": True, "response": g.user})
