from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.models import Privilegies
from src.services import AuthAdminService
from src.services import PlanService


router = Blueprint(name="PlanAdmin", import_name=__name__)

# Decorador
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


# Decorador
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


# Decorator
def has_access(func, access_level):
    @wraps(func)
    def wrap(*arg, **kwargs):
        user = g.admin["b"]

        if not user.has_access(access_level.value):
            abort(
                401,
                description="Unauthorized",
                response="You not enough permissions to access",
            )

    return wrap


# GET: /api/v1/admin/plan/<int:_id>
@router.route("/<int:_id>", methods=["GET"])
@login_required
def index_plan_admin_one(_id):
    service = PlanService()
    plan = service.get(_id)

    return jsonify({"success": True, "response": plan})


# GET: /api/v1/admin/plan
@router.route("/", methods=["GET"])
@login_required
def index_plan_admin():
    page = request.args.get("page") or 1
    per_pages = request.args.get("per_pages")

    service = PlanService()
    plans = service.list(page, per_pages)

    return jsonify({"success": True, "response": plans})


# POST: /api/v1/admin/plan
@router.route("/", methods=["POST"])
@login_required
def register_plan_admin():
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = PlanService()
    plan = service.create(body)

    return jsonify({"success": True, "response": plan})


# PUT: /api/v1/admin/plan/<int:_id>
@router.route("/<int:_id>", methods=["PUT"])
@login_required
def update_plan_admin(uid):
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = PlanService()
    plan = service.update(_id, body)

    return jsonify({"success": True, "response": plan})


# PATCH: /api/v1/admin/plan/<int:_id>
@router.route("/<int:_id>", methods=["PATCH"])
@login_required
def update_field_plan_admin(_id):
    body = request.get_json()

    if not body:
        return abort(400, description="NotFoundData", response="not-found-data")

    service = PlanService()
    plan = service.update_field(_id, body)

    return jsonify({"success": True, "response": plan})


# PATCH /api/v1/admin/plan/disabled/<int:_id>
@router.route("/disabled/<int:_id>", methods=["PATCH"])
@login_required
def disabled_plan_admin(_id):
    service = PlanService()
    plan = service.disabled(_id)

    return jsonify({"success": True, "response": plan})


# DELETE: /api/v1/admin/plan/<int:_id>
@router.route("/<int:_id>", methods=["DELETE"])
@login_required
def delete_plan_admin(_id):
    service = PlanService()
    plan = service.delete(_id)

    return jsonify({"success": True, "response": plan})
