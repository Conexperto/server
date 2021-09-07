"""
    Blueprint Speciality
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import login_required
from src.services import SpecialityService


router = Blueprint(name="SpecialityAdmin", import_name=__name__)


@router.route("/<uid>", methods=["GET"])
@login_required(admin=True)
def index_speciality_admin_one(uid):
    """
    GET: /api/v1/admin/speciality/<uid>
    """
    try:
        service = SpecialityService()
        speciality = service.get(uid)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_speciality_admin():
    """
    GET: /api/v1/admin/speciality
    """
    try:
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = SpecialityService()
        specialities = service.list(search, page, per_pages, order_by, order)

        return jsonify({"success": True, "response": specialities})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["POST"])
@login_required(admin=True)
def register_speciality_admin():
    """
    POST: /api/v1/admin/speciality
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = SpecialityService()
        speciality = service.create(body)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PUT"])
@login_required(admin=True)
def update_speciality_admin(uid):
    """
    PUT: /api/v1/admin/speciality/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = SpecialityService()
        speciality = service.update(uid, body)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PATCH"])
@login_required(admin=True)
def update_field_speciality_admin(uid):
    """
    PATCH: /api/v1/admin/speciality/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = SpecialityService()
        speciality = service.update_field(uid, body)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required(admin=True)
def disabled_speciality_admin(uid):
    """
    PATCH: /api/v1/admin/speciality/disabled/<uid>
    """
    try:
        service = SpecialityService()
        speciality = service.disabled(uid)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["DELETE"])
@login_required(admin=True)
def delete_speciality_admin(uid):
    """
    DELETE: /api/v1/admin/speciality/<uid>
    """
    try:
        service = SpecialityService()
        speciality = service.delete(uid)

        return jsonify({"success": True, "response": speciality})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))
