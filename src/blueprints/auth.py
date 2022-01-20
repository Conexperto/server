""" src.blueprints.auth """
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.middlewares import login_required
from src.services import AuthService


router = Blueprint(name="Auth", import_name=__name__)


@router.route("/", methods=["GET"])
@login_required()
def index_auth():
    """
    GET: /api/v1/auth
    """
    return jsonify({"success": True, "response": g.user})


@router.route("/specialities", methods=["GET"])
@login_required()
def index_auth_specialities():
    """
    GET: /api/v1/auth/specialities
    """
    user = g.user["b"]
    specialities = user.specialities
    return jsonify({"success": True, "response": specialities})


@router.route("/methods", methods=["GET"])
@login_required()
def index_auth_methods():
    """
    GET: /api/v1/auth/methods
    """
    user = g.user["b"]
    methods = user.methods
    return jsonify({"success": True, "response": methods})


@router.route("/", methods=["POST"])
def register_auth():
    """
    POST: /api/v1/auth
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        if not isinstance(body, dict):
            raise HandlerException(400, "Body must be a object")

        service = AuthService()
        user = service.create(body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/", methods=["PUT"])
@login_required()
def update_auth():
    """
    PUT: /api/v1/auth
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body reequest")

        if not isinstance(body, dict):
            raise HandlerException(400, "Body must be a object")

        service = AuthService()
        user = service.update(g.user, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/specialities", methods=["PUT"])
@login_required()
def update_auth_specialities():
    """
    PUT: /api/v1/auth/specialities
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        if not isinstance(body, list):
            raise HandlerException(400, "Body must be a array")

        service = AuthService()
        user = service.update(g.user, {"specialities": body})

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/methods", methods=["PUT"])
@login_required()
def update_auth_method():
    """
    PUT: /api/v1/auth/methods
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        if not isinstance(body, list):
            raise HandlerException(400, "Body must be a array")

        service = AuthService()
        user = service.update(g.user, {"methods": body})

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/plans", methods=["PUT"])
@login_required()
def update_auth_plan():
    """
    PUT: /api/v1/auth/plans
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        if not isinstance(body, list):
            raise HandlerException(400, "Body must be a array")

        service = AuthService()
        user = service.update(g.user, {"plans": body})

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/", methods=["PATCH"])
@login_required()
def update_field_auth():
    """
    PATCH: /api/v1/auth
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        if not isinstance(body, dict):
            raise HandlerException(400, "Body must be a object")

        service = AuthService()
        user = service.update_field(g.user, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()


@router.route("/disabled", methods=["PATCH"])
@login_required()
def disabled_auth():
    """
    PATCH /api/v1/auth/disabled
    """
    try:
        service = AuthService()
        user = service.disabled(g.user)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(
            500, "Unexpected response: " + str(ex), str(ex)
        ).abort()
