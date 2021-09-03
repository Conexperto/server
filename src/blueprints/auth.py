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


@router.route("/", methods=["POST"])
def register_auth():
    """
    POST: /api/v1/auth
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body request")

        service = AuthService()
        user = service.create(body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, str(ex)).abort()


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

        service = AuthService()
        user = service.update(g.user, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, str(ex)).abort()


# @router.route("/expert", methods=["PUT"])
# @login_required()
# def update_auth_expert():
#    """
#    PUT: /api/v1/auth/expert
#    """
#    body = request.get_json()
#
#    if not body:
#        return abort(400, description="NotFoundData", response="not-found-data")
#
#    _expert = g.user["b"].expert
#
#    if hasattr(body, "speciality"):
#        ass_speciality = AssociationExpertToSpecialityService()
#        ass_speciality.update_or_create_and_delete_many(_expert.id, body["speciality"])
#
#    if hasattr(body, "method"):
#        ass_method = AssociationExpertToMethodService()
#        ass_method.update_or_create_and_delete_many(_expert.id, body["method"])
#
#    if hasattr(body, "plan"):
#        plan = PlanService()
#        plan.update_or_create_and_delete_many(_expert.id, body["plan"])
#
#    service = ExpertService()
#    expert = service.update(_expert.id, body)
#
#    return jsonify({"success": True, "response": expert})


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

        service = AuthService()
        user = service.update_field(g.user, body)

        return jsonify({"success": True, "response": user})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, str(ex)).abort()


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
        HandlerException(500, str(ex)).abort()
