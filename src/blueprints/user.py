""" src.blueprints.user """
from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request
from src.services import AuthService
from src.services import UserService


router = Blueprint(name="User", import_name=__name__)


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
        g.admin = service.authentication(id_token)
        return func(*args, **kwargs)

    return wrap


@router.route("/<uid>", methods=["GET"])
@login_required
def index_user_one(uid):
    """
    GET: /api/v1/user/<uid>
    """
    service = UserService()
    user = service.get(uid)

    return jsonify({"success": True, "response": user})


@router.route("/", methods=["GET"])
@login_required
def index_user():
    """
    GET: /api/v1/user
    """
    page = request.args.get("page") or 1
    per_pages = request.args.get("per_pages")

    service = UserService()
    users = service.list(page, per_pages)

    return jsonify({"success": True, "response": users})
